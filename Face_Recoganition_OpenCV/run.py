import Interface_excel as Interface
import sys

if __name__ == "__main__":
    confidence_match = 0.4
    confidence_save = 0.4
    confidence_show = True
    
    if len(sys.argv) > 1:
        if sys.argv[1] and sys.argv[1].lower() == 'false':  # Fix: Add () for method call
            confidence_show = False
        if len(sys.argv) > 2 and sys.argv[2]:  # Fix: Check bounds
            confidence_match = (100-float(sys.argv[2]))/100
        if len(sys.argv) > 3 and sys.argv[3]:  # Fix: Check bounds
            confidence_save = (100-float(sys.argv[3]))/100
        elif len(sys.argv) > 2 and sys.argv[2]:  # Fix: Check bounds
            confidence_save = (100-float(sys.argv[2]))/100
            
    Interface.interFace(confidence_match, confidence_save, confidence_show)