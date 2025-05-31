import Interface_excel as Interface
import sys

if __name__ == "__main__":
    confidence_match = 0.4
    confidence_save = 0.4
    confidence_show = True
    excel_path = None
    
    if len(sys.argv) > 1:
        if sys.argv[1]:
            excel_path = sys.argv[1]
        if len(sys.argv) >2 and sys.argv[2] and sys.argv[2].lower() == 'false':  # Fix: Add () for method call
            confidence_show = False
        if len(sys.argv) > 3 and sys.argv[3]:  # Fix: Check bounds
            confidence_match = (100-float(sys.argv[3]))/100
        if len(sys.argv) > 4 and sys.argv[4]:  # Fix: Check bounds
            confidence_save = (100-float(sys.argv[4]))/100
        elif len(sys.argv) > 3 and sys.argv[3]:  # Fix: Check bounds
            confidence_save = (100-float(sys.argv[3]))/100
            
    Interface.interFace(excel_path , confidence_match, confidence_save, confidence_show)