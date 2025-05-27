import Interface
import sys

if __name__ == "__main__":
    confidence_match = 0.4
    confidence_save = 0.4
    confidence_show = True
    if(len(sys.argv) > 1):
        if(sys.argv[1] and sys.argv[1].lower == 'false'):
                confidence_show = False
        if(sys.argv[2]):
            confidence_match = (100-float(sys.argv[2]))/100
        if(sys.argv[3]):
            confidence_save = (100-float(sys.argv[3]))/100
        elif(sys.argv[2]):
            confidence_save = (100-float(sys.argv[2]))/100
    Interface.interFace(confidence_match,confidence_save,confidence_show)