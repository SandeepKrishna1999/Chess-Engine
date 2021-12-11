import graphics
from graphics import *
import chess


def fen_converter(ip):
    output=' '
    for i in range(len(ip)):
        if ip[i]==' ':
            break
        if ip[i]=='/':
            continue
        if ip[i]=='8':
            output=output+'11111111'
        if ip[i]=='7':
            output=output+'1111111'
        if ip[i]=='6':
            output=output+'111111'
        if ip[i]=='5':
            output=output+'11111'
        if ip[i]=='4':
            output=output+'1111'
        if ip[i]=='3':
            output=output+'111'
        if ip[i]=='2':
            output=output+'11'
        if ip[i]=='1':
            output=output+'1'
        if ip[i]=='r':
            output=output+'r'
        if ip[i]=='n':
            output=output+'n'
        if ip[i]=='b':
            output=output+'b'
        if ip[i]=='q':
            output=output+'q'
        if ip[i]=='k':
            output=output+'k'
        if ip[i]=='R':
            output=output+'R'
        if ip[i]=='N':
            output=output+'N'
        if ip[i]=='B':
            output=output+'B'
        if ip[i]=='Q':
            output=output+'Q'
        if ip[i]=='K':
            output=output+'K'
        if ip[i]=='p':
            output=output+'p'
        if ip[i]=='P':
            output=output+'P'
    return output

def chess_board():
    BOARD = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    
    length=400
    board=graphics.GraphWin('Chess Board',410,410)
    sq_len=length/8

    define_x_pts=[] #all the x cordinates which corresponds to the centers if every square
    x_var=25
    for i in range(8):
        x_var=x_var
        define_x_pts.append(x_var)
        x_var=x_var+sq_len

    define_y_pts=[] #all the y cordinates which corresponds to the centers if every square
    y_var=25
    for i in range(8):
        y_var=y_var
        define_y_pts.append(y_var)
        y_var=y_var+sq_len

    y_pt=0
    for i in range(8):

        if i%2==0:
            x_pt=sq_len
            for j in range(8):
                square=Rectangle(Point(x_pt,y_pt), Point(x_pt+sq_len,y_pt+sq_len))
                square.setFill('black')
                square.draw(board)
                x_pt=x_pt+(2*sq_len)
                if j==7:
                    break
                

        if i%2!=0:
            x_pt=0
            for j in range(8):
                square=Rectangle(Point(x_pt,y_pt), Point(x_pt+sq_len,y_pt+sq_len))
                square.setFill('black')
                square.draw(board)
                x_pt=x_pt+(2*sq_len)
                if x_pt==length:
                    break

        y_pt=y_pt+sq_len

        x_end=405
        y_start=length/16
        for i in range(8):
            TXT=str(8-i)
            text=Text(Point(x_end,y_start),TXT)
            text.draw(board)
            y_start=y_start+sq_len

        y_end=405
        Letter=['a','b','c','d','e','f','g','h']
        x_start=length/16
        for i in range(8):
            TXT=Letter[i]
            text=Text(Point(x_start,y_end),TXT)
            text.draw(board)
            x_start=x_start+sq_len
            
    pawn=0
    PAWN=0 
    rook=0
    ROOK=0
    bishop=0
    BISHOP=0
    knight=0
    KNIGHT=0
    queen=0
    QUEEN=0
    king=0
    KING=0
    

    
    board_data=fen_converter(BOARD.fen())
   
    
    ### display board from the variable board_data
    for i in range(len(board_data)):
        
        x_var=(i%8)
        y_var=int(i/8)
        if (i%8)==0:
            x_var=8
            y_var=y_var-1
        
        
        x_pt=x_var-1
        y_pt=y_var
        
        if i==64:
            y_pt=7
            x_pt=7
        
        if board_data[i]=='r':
              while True:  
                if rook==0:
                    blue_rook1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Rook.gif")
                    blue_rook1.draw(board)
                    rook=rook+1 
                    break
                if rook==1:      
                    blue_rook2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Rook.gif")
                    blue_rook2.draw(board)
                    rook=rook+1  
                    break
                continue
            
        if board_data[i]=='n':
            while True:
                if knight==0:
                    blue_knight1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Knight.gif")
                    blue_knight1.draw(board)
                    knight=knight+1
                    break
                if knight==1:
                    blue_knight2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Knight.gif")
                    blue_knight2.draw(board)
                    knight=knight+1
                    break
            continue
            
        if board_data[i]=='b':
            while True:
                if bishop==0:
                    blue_bishop1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Bishop.gif")
                    blue_bishop1.draw(board)
                    bishop=bishop+1
                    break      
                if bishop==1:
                    blue_bishop2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Bishop.gif")
                    blue_bishop2.draw(board)
                    bishop=bishop+1
                    break
            continue
            
        if board_data[i]=='q':
            blue_queen = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Queen.gif")
            blue_queen.draw(board)
            queen=1
            continue
            
        if board_data[i]=='k':
            blue_king = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_King.gif")
            blue_king.draw(board)
            king=1
            continue
                   
        if board_data[i]=='p':
            while True:
                if pawn==0:
                    blue_pawn1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn1.draw(board)
                    pawn=pawn+1
                    break
                
                if pawn==1:
                    blue_pawn2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn2.draw(board)
                    pawn=pawn+1
                    break
                    
                if pawn==2:
                    blue_pawn3 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn3.draw(board)
                    pawn=pawn+1
                    break
                    
                if pawn==3:
                    blue_pawn4 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn4.draw(board)
                    pawn=pawn+1
                    break
                    
                if pawn==4:
                    blue_pawn5 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn5.draw(board)
                    pawn=pawn+1
                    break
                    
                if pawn==5:
                    blue_pawn6 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn6.draw(board)
                    pawn=pawn+1
                    break
                
                if pawn==6:
                    blue_pawn7 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn7.draw(board)
                    pawn=pawn+1
                    break
            
                if pawn==7:
                    blue_pawn8 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                    blue_pawn8.draw(board)
                    pawn=pawn+1
                    break
            continue
            
        if board_data[i]=='R':
            while True: 
                print(ROOK)
                if ROOK==0:
                    red_rook1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Rook.gif")
                    red_rook1.draw(board)
                    ROOK=ROOK+1
                    break
                if ROOK==1:
                    red_rook2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Rook.gif")
                    red_rook2.draw(board)
                    ROOK=ROOK+1
                    break
            continue
               
        if board_data[i]=='N':
            while True:
                if KNIGHT==0:
                    red_knight1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Knight.gif")
                    red_knight1.draw(board)
                    KNIGHT=KNIGHT+1
                    break
                    
                if KNIGHT==1:
                    red_knight2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Knight.gif")
                    red_knight2.draw(board)
                    KNIGHT=KNIGHT+1
                    break
            continue
            
        if board_data[i]=='B':
            while True:
                if BISHOP==0:
                    red_bishop1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Bishop.gif")
                    red_bishop1.draw(board)
                    BISHOP=BISHOP+1
                    break
                
                if BISHOP==1:
                    red_bishop2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Bishop.gif")
                    red_bishop2.draw(board)
                    BISHOP=BISHOP+1
                    break
            continue
            
        if board_data[i]=='Q':
            red_queen = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Queen.gif")
            red_queen.draw(board)
            QUEEN=1
            continue
            
        if board_data[i]=='K':
            red_king = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_King.gif")
            red_king.draw(board)
            KING=1
            continue
                    
        if board_data[i]=='P':
            while True:
                if PAWN==0:
                    red_pawn1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn1.draw(board)
                    PAWN=PAWN+1
                    break
                   
                if PAWN==1:
                    red_pawn2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn2.draw(board)
                    PAWN=PAWN+1
                    break
                    
                if PAWN==2:
                    red_pawn3 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn3.draw(board)
                    PAWN=PAWN+1
                    break
                    
                if PAWN==3:
                    red_pawn4 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn4.draw(board)
                    PAWN=PAWN+1
                    break
                    
                if PAWN==4:
                    red_pawn5 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn5.draw(board)
                    PAWN=PAWN+1
                    break
                    
                if PAWN==5:
                    red_pawn6 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn6.draw(board)
                    PAWN=PAWN+1
                    break
                
                if PAWN==6:
                    red_pawn7 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn7.draw(board)
                    PAWN=PAWN+1
                    break
                    
                if PAWN==7:
                    red_pawn8 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                    red_pawn8.draw(board)
                    PAWN=PAWN+1
                    break
                
            continue
            
    p = input("Enter your move: ")
    while p!="end":
                if pawn==8:
                    blue_pawn1.undraw()
                    blue_pawn2.undraw()
                    blue_pawn3.undraw()
                    blue_pawn4.undraw()
                    blue_pawn5.undraw()
                    blue_pawn6.undraw()
                    blue_pawn7.undraw()
                    blue_pawn8.undraw()
                    
                if pawn==7:
                    blue_pawn1.undraw()
                    blue_pawn2.undraw()
                    blue_pawn3.undraw()
                    blue_pawn4.undraw()
                    blue_pawn5.undraw()
                    blue_pawn6.undraw()
                    blue_pawn7.undraw()
                    
                if pawn==6:
                    blue_pawn1.undraw()
                    blue_pawn2.undraw()
                    blue_pawn3.undraw()
                    blue_pawn4.undraw()
                    blue_pawn5.undraw()
                    blue_pawn6.undraw()
                    
                if pawn==5:
                    blue_pawn1.undraw()
                    blue_pawn2.undraw()
                    blue_pawn3.undraw()
                    blue_pawn4.undraw()
                    blue_pawn5.undraw()
                
                if pawn==4:
                    blue_pawn1.undraw()
                    blue_pawn2.undraw()
                    blue_pawn3.undraw()
                    blue_pawn4.undraw()
                    
                if pawn==3:
                    blue_pawn1.undraw()
                    blue_pawn2.undraw()
                    blue_pawn3.undraw()
                
                if pawn==2:
                    blue_pawn1.undraw()
                    blue_pawn2.undraw()
                    
                if pawn==1:
                    blue_pawn1.undraw()
                
                pawn=0
                
                if PAWN==8:
                    red_pawn1.undraw()
                    red_pawn2.undraw()
                    red_pawn3.undraw()
                    red_pawn4.undraw()
                    red_pawn5.undraw()
                    red_pawn6.undraw()
                    red_pawn7.undraw()
                    red_pawn8.undraw()
                    
                if PAWN==7:
                    red_pawn1.undraw()
                    red_pawn2.undraw()
                    red_pawn3.undraw()
                    red_pawn4.undraw()
                    red_pawn5.undraw()
                    red_pawn6.undraw()
                    red_pawn7.undraw()
                    
                if PAWN==6:
                    red_pawn1.undraw()
                    red_pawn2.undraw()
                    red_pawn3.undraw()
                    red_pawn4.undraw()
                    red_pawn5.undraw()
                    red_pawn6.undraw()
                    
                if PAWN==5:
                    red_pawn1.undraw()
                    red_pawn2.undraw()
                    red_pawn3.undraw()
                    red_pawn4.undraw()
                    red_pawn5.undraw()
                
                if PAWN==4:
                    red_pawn1.undraw()
                    red_pawn2.undraw()
                    red_pawn3.undraw()
                    red_pawn4.undraw()
                    
                if PAWN==3:
                    red_pawn1.undraw()
                    red_pawn2.undraw()
                    red_pawn3.undraw()
                    
                if PAWN==2:
                    red_pawn1.undraw()
                    red_pawn2.undraw()
                    
                if PAWN==1:
                    red_pawn1.undraw()
                
                PAWN=0
                    
                if rook == 2:
                    blue_rook1.undraw()
                    blue_rook2.undraw()
                    
                if rook == 1:
                    blue_rook1.undraw()
                
                rook=0
                
                if ROOK== 2:
                    red_rook1.undraw()
                    red_rook2.undraw()
                    
                if ROOK == 1:
                    red_rook1.undraw()
                
                ROOK=0
                
                if bishop==2:
                    blue_bishop1.undraw()
                    blue_bishop2.undraw()
                    
                if bishop==1:
                    blue_bishop1.undraw()
                    
                bishop=0
                
                if BISHOP==2:
                    red_bishop1.undraw()
                    red_bishop2.undraw()
                    
                if BISHOP==1:
                    red_bishop1.undraw()
                    
                BISHOP=0
                    
                if knight==2:
                    blue_knight1.undraw()
                    blue_knight2.undraw()
                    
                if knight==1:
                    blue_knight1.undraw()
                    
                knight=0
                
                if KNIGHT==2:
                    red_knight1.undraw()
                    red_knight2.undraw()
                    
                if KNIGHT==1:
                    red_knight1.undraw()
                    
                KNIGHT=0
                
                if queen==1:
                    blue_queen.undraw()
                
                queen=0
                
                if QUEEN==1:
                    red_queen.undraw()
                
                QUEEN=0
                
                if king==1:
                    blue_king.undraw()
                    
                king=0
                
                if KING==1:
                    red_king.undraw()
                    
                KING=0
                
                move = chess.Move.from_uci(str(BOARD.parse_san(p)))
                BOARD.push(move)
                
                board_data=fen_converter(BOARD.fen())
                
                ### display board from the variable board_data
                for i in range(len(board_data)):
                    
                    x_var=(i%8)
                    y_var=int(i/8)
                    if (i%8)==0:
                        x_var=8
                        y_var=y_var-1
                    
                    
                    x_pt=x_var-1
                    y_pt=y_var
                    
                    if i==64:
                        y_pt=7
                        x_pt=7
                    
                    if board_data[i]=='r':
                          while True:  
                            if rook==0:
                                blue_rook1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Rook.gif")
                                blue_rook1.draw(board)
                                rook=rook+1 
                                break
                            if rook==1:      
                                blue_rook2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Rook.gif")
                                blue_rook2.draw(board)
                                rook=rook+1  
                                break
                            continue
                        
                    if board_data[i]=='n':
                        while True:
                            if knight==0:
                                blue_knight1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Knight.gif")
                                blue_knight1.draw(board)
                                knight=knight+1
                                break
                            if knight==1:
                                blue_knight2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Knight.gif")
                                blue_knight2.draw(board)
                                knight=knight+1
                                break
                        continue
                        
                    if board_data[i]=='b':
                        while True:
                            if bishop==0:
                                blue_bishop2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Bishop.gif")
                                blue_bishop2.draw(board)
                                bishop=bishop+1
                                break      
                            if bishop==1:
                                blue_bishop2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Bishop.gif")
                                blue_bishop2.draw(board)
                                bishop=bishop+1
                                break
                        continue
                        
                    if board_data[i]=='q':
                        blue_queen = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Queen.gif")
                        blue_queen.draw(board)
                        queen=1
                        continue
                        
                    if board_data[i]=='k':
                        blue_king = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_King.gif")
                        blue_king.draw(board)
                        king=1
                        continue
                               
                    if board_data[i]=='p':
                        while True:
                            if pawn==0:
                                blue_pawn1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn1.draw(board)
                                pawn=pawn+1
                                break
                            
                            if pawn==1:
                                blue_pawn2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn2.draw(board)
                                pawn=pawn+1
                                break
                                
                            if pawn==2:
                                blue_pawn3 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn3.draw(board)
                                pawn=pawn+1
                                break
                                
                            if pawn==3:
                                blue_pawn4 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn4.draw(board)
                                pawn=pawn+1
                                break
                                
                            if pawn==4:
                                blue_pawn5 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn5.draw(board)
                                pawn=pawn+1
                                break
                                
                            if pawn==5:
                                blue_pawn6 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn6.draw(board)
                                pawn=pawn+1
                                break
                            
                            if pawn==6:
                                blue_pawn7 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn7.draw(board)
                                pawn=pawn+1
                                break
                        
                            if pawn==7:
                                blue_pawn8 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Blue_Pawn.gif")
                                blue_pawn8.draw(board)
                                pawn=pawn+1
                                break
                        continue
                        
                    if board_data[i]=='R':
                        while True:  
                            if ROOK==0:
                                red_rook1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Rook.gif")
                                red_rook1.draw(board)
                                ROOK=ROOK+1
                                break
                            if ROOK==1:
                                red_rook2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Rook.gif")
                                red_rook2.draw(board)
                                ROOK=ROOK+1
                                break
                        continue
                           
                    if board_data[i]=='N':
                        while True:
                            if KNIGHT==0:
                                red_knight1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Knight.gif")
                                red_knight1.draw(board)
                                KNIGHT=KNIGHT+1
                                break
                                
                            if KNIGHT==1:
                                red_knight2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Knight.gif")
                                red_knight2.draw(board)
                                KNIGHT=KNIGHT+1
                                break
                        continue
                        
                    if board_data[i]=='B':
                        while True:
                            if BISHOP==0:
                                red_bishop1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Bishop.gif")
                                red_bishop1.draw(board)
                                BISHOP=BISHOP+1
                                break
                            
                            if BISHOP==1:
                                red_bishop2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Bishop.gif")
                                red_bishop2.draw(board)
                                BISHOP=BISHOP+1
                                break
                        continue
                        
                    if board_data[i]=='Q':
                        red_queen = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Queen.gif")
                        red_queen.draw(board)
                        QUEEN=1
                        continue
                        
                    if board_data[i]=='K':
                        red_king = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_King.gif")
                        red_king.draw(board)
                        KING=1
                        continue
                                
                    if board_data[i]=='P':
                        while True:
                            if PAWN==0:
                                red_pawn1 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn1.draw(board)
                                PAWN=PAWN+1
                                break
                               
                            if PAWN==1:
                                red_pawn2 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn2.draw(board)
                                PAWN=PAWN+1
                                break
                                
                            if PAWN==2:
                                red_pawn3 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn3.draw(board)
                                PAWN=PAWN+1
                                break
                                
                            if PAWN==3:
                                red_pawn4 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn4.draw(board)
                                PAWN=PAWN+1
                                break
                                
                            if PAWN==4:
                                red_pawn5 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn5.draw(board)
                                PAWN=PAWN+1
                                break
                                
                            if PAWN==5:
                                red_pawn6 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn6.draw(board)
                                PAWN=PAWN+1
                                break
                            
                            if PAWN==6:
                                red_pawn7 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn7.draw(board)
                                PAWN=PAWN+1
                                break
                                
                            if PAWN==7:
                                red_pawn8 = Image(Point(define_x_pts[x_pt],define_y_pts[y_pt]),"Red_Pawn.gif")
                                red_pawn8.draw(board)
                                PAWN=PAWN+1
                                break
                            
                        continue
                p = input('Enter your move: ')
                
    return

chess_board()