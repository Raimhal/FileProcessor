

def log_detections(logger,detections):
    for text in detections:
        logger('-' * 100)
        logger(f'Text: {text["DetectedText"]}')
        logger(f'Confidence: {text["Confidence"]:.2f}%')
        logger(f'Type: {text["Type"]}')
    logger('-' * 100)