from detections import Detection

detector = Detection()

preds2 = detector.detect_troops()
print(preds2)
for p in preds2:
    print(p['class'])

preds1 = detector.detect_card(0)  
print(preds1)  
for p in preds1:
    print(p['class'])
    print(p['class_id'])

preds1 = detector.detect_card(1)    
for p in preds1:
    print(p['class'])

preds1 = detector.detect_card(2)    
for p in preds1:
    print(p['class'])

