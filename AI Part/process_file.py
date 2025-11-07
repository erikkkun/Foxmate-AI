"""
Data processing script - analyzes data using trained model
Compatible with GPU-accelerated AI.py
"""

import json
import sys
from typing import Optional

# Fix pickle loading issue - needed even when running as main
if __name__ == '__main__':
    import AI
    # Make sure pickle can find the right module
    sys.modules['__main__'] = AI

try:
    from AI import FocusClassifier
except ImportError:
    print("Error: Can't import AI module")
    print("   Make sure AI.py is in the same directory")
    sys.exit(1)


def process_data(input_file: str, output_file: str, verbose: bool = True):
    """
    Read data file, analyze with AI, output reminders and suggestions

    Args:
        input_file: Input file path (one JSON object per line)
        output_file: Output file path
        verbose: Show detailed progress
    """
    if verbose:
        print("=" * 60)
        print("Focus Analysis Processing")
        print("=" * 60)

    # Load model
    if verbose:
        print("\nLoading AI model...")

    try:
        classifier = FocusClassifier(use_gpu=False)  # CPU is fine for inference
        classifier.load_model('focus_model.pkl')

        if verbose:
            print("Model loaded successfully!")
    except FileNotFoundError:
        print("\nError: Model file focus_model.pkl not found")
        print("   Please run AI.py first to train the model")
        return False
    except Exception as e:
        print(f"\nFailed to load model: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Process data
    if verbose:
        print(f"\nReading data: {input_file}")

    try:
        with open(input_file, 'r', encoding='utf-8') as input_f:
            lines = [line.strip() for line in input_f if line.strip()]

        if verbose:
            print(f"Found {len(lines)} data points")
    except FileNotFoundError:
        print(f"\nError: Input file not found: {input_file}")
        return False
    except Exception as e:
        print(f"\nFailed to read file: {e}")
        return False

    # Analyze data
    if verbose:
        print(f"\nStarting analysis...")

    results = []
    count_success = 0
    count_focused = 0
    count_unfocused = 0

    for i, line in enumerate(lines, 1):
        try:
            # Parse data
            data = json.loads(line)

            # AI analysis
            prediction, probability = classifier.predict(data)
            reminder = classifier.get_reminder(data, prediction, probability)

            # Track stats
            count_success += 1
            if prediction == 1:
                count_focused += 1
            else:
                count_unfocused += 1

            # Save result
            result = {
                'index': i,
                'title': data.get('title', 'Unknown'),
                'app': data.get('app', 'Unknown'),
                'status': reminder['status'],
                'confidence': reminder['confidence'],
                'message': reminder['message'],
                'suggestion': reminder.get('suggestion', '')
            }
            results.append(result)

            # Show progress
            if verbose and i % 10 == 0:
                print(f"   Processed: {i}/{len(lines)}")

        except json.JSONDecodeError:
            if verbose:
                print(f"Skipping line {i}: Invalid JSON format")
            continue
        except KeyError as e:
            if verbose:
                print(f"Skipping line {i}: Missing field {e}")
            continue
        except Exception as e:
            if verbose:
                print(f"Skipping line {i}: {e}")
            continue

    # Save results
    if verbose:
        print(f"\nSaving results: {output_file}")

    try:
        with open(output_file, 'w', encoding='utf-8') as output_f:
            # Write summary
            output_f.write("=" * 60 + "\n")
            output_f.write("Focus Analysis Report\n")
            output_f.write("=" * 60 + "\n\n")
            output_f.write(f"Total data points: {len(lines)}\n")
            output_f.write(f"Successfully analyzed: {count_success}\n")
            output_f.write(f"Focused: {count_focused} ({count_focused / count_success * 100:.1f}%)\n")
            output_f.write(f"Distracted: {count_unfocused} ({count_unfocused / count_success * 100:.1f}%)\n")
            output_f.write("\n" + "=" * 60 + "\n\n")

            # Write detailed results
            for result in results:
                output_f.write(f"[{result['index']}] {result['title']}\n")
                output_f.write(f"App: {result['app']}\n")
                output_f.write(f"Status: {result['status']} (confidence: {result['confidence']:.1f}%)\n")
                output_f.write(f"{result['message']}\n")
                if result['suggestion']:
                    output_f.write(f"{result['suggestion']}\n")
                output_f.write("\n" + "-" * 60 + "\n\n")

        if verbose:
            print("Results saved successfully!")
    except Exception as e:
        print(f"\nFailed to save results: {e}")
        return False

    # Show summary
    if verbose:
        print("\n" + "=" * 60)
        print("Processing Summary")
        print("=" * 60)
        print(f"Total data points: {len(lines)}")
        print(f"Successfully analyzed: {count_success}")
        print(f"Focused: {count_focused} ({count_focused / count_success * 100:.1f}%)")
        print(f"Distracted: {count_unfocused} ({count_unfocused / count_success * 100:.1f}%)")
        print("=" * 60)
        print(f"\nDone! Results saved to: {output_file}")

    return True


def process_single_activity(data: dict, classifier: Optional[FocusClassifier] = None) -> Optional[dict]:
    """
    Analyze a single activity data point

    Args:
        data: Activity data dictionary
        classifier: Classifier instance (optional, will create new one if not provided)

    Returns:
        Analysis result dictionary, or None if failed
    """
    if classifier is None:
        classifier = FocusClassifier(use_gpu=False)
        try:
            classifier.load_model('focus_model.pkl')
        except:
            return None

    try:
        prediction, probability = classifier.predict(data)
        reminder = classifier.get_reminder(data, prediction, probability)

        return {
            'status': reminder['status'],
            'is_focused': prediction == 1,
            'confidence': reminder['confidence'],
            'message': reminder['message'],
            'suggestion': reminder.get('suggestion', ''),
            'probabilities': {
                'unfocused': probability[0],
                'focused': probability[1]
            }
        }
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None


if __name__ == "__main__":
    # Default file paths
    INPUT_FILE = 'input_data.txt'
    OUTPUT_FILE = 'result.txt'

    # Support command line arguments
    if len(sys.argv) >= 2:
        INPUT_FILE = sys.argv[1]
    if len(sys.argv) >= 3:
        OUTPUT_FILE = sys.argv[2]

    print("\nUsage:")
    print(f"  python process_file.py [input_file] [output_file]")
    print(f"\nCurrent configuration:")
    print(f"  Input file: {INPUT_FILE}")
    print(f"  Output file: {OUTPUT_FILE}\n")

    # Run processing
    success = process_data(INPUT_FILE, OUTPUT_FILE)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)