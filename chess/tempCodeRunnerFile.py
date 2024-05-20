mode = ""
            #! display man hinh khoi dong chuong trinh
        
            #! biến human_turn để biết có phải là người chơi hay không (chế độ người chơi hay máy chơi)
            if (game_state.trangDiChuyen and player_one == True) or (not game_state.trangDiChuyen and player_two == True):
                human_turn = True
            else:
                human_turn = False
            
            for e in p.event.get():    
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if homebutton.isMouseOnText() == True: 
                        clock = p.time.Clock()
                        beginScreen = True
                        running = False
                        break
                        
                        
                    if not game_over:
                        location = p.mouse.get_pos()  # (x, y) location of the mouse
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE
                        if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # append for both 1st and 2nd click
                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    square_selected = ()  # reset user clicks
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]

                # key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        game_state.undoMove()
                        move_made = True
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_r:  # reset the game when 'r' is pressed
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True

            # AI move finder
            if not game_over and not human_turn and not move_undone:
                if not ai_thinking:
                    ai_thinking = True
                    return_queue = Queue()  # used to pass data between threads
                    move_finder_process = Process(target=target, args=(game_state, valid_moves, return_queue))
                    move_finder_process.start()

                if not move_finder_process.is_alive():
                    ai_move = return_queue.get()
                    if ai_move is None:
                        ai_move = ChessAI.findRandomMove(valid_moves)
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                    ai_thinking = False

            if move_made:
                if animate:
                    animateMove(game_state.move_log[-1], screen, game_state.board, clock)
                valid_moves = game_state.getValidMoves()
                move_made = False
                animate = False
                move_undone = False

            
            drawGameState(screen, game_state, valid_moves, square_selected)

            if not game_over:
                drawMoveLog(screen, game_state, move_log_font)

            if game_state.checkmate:
                game_over = True
                if game_state.trangDiChuyen:
                    drawEndGameText(screen, "Black wins by checkmate")
                else:
                    drawEndGameText(screen, "White wins by checkmate")

            elif game_state.stalemate:
                game_over = True
                drawEndGameText(screen, "Stalemate")
            
            

            playtime = Button.Button('playtime', (60, 150), (400, 200))
            if  time <= p.time.get_ticks() and p.time.get_ticks() <= time + 2000:
                playtime.displayButton(screen)
            
            homebutton = Button.Button('homebutton', (560, 452), (50, 50))
            helpbutton = Button.Button('help', (640, 430), (90, 90))
            twoplayermode = Button.Button('twoplayermode', (60, 150), (400, 200))
            playcommode = Button.Button('playcommode', (60, 150), (400, 200))
            twocommode = Button.Button('twocommode', (60, 150), (400, 200))

            if helpbutton.isMouseOnText() == True:
          