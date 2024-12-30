from tkinter import Tk, Canvas, Label, Button

# Vars
score = 0
highscore = 0
all_blocks = []

# Making the main window
window = Tk()
window.title("Breakout Game")
x_speed = 5
y_speed = -5


# Making the functionality

def making_blocks():
    global all_blocks
    # Odd rows of blocks
    x1 = 0
    x2 = 70
    for i in range(9):
        all_blocks.append(canvas.create_rectangle((x1, 70), (x2, 100), fill="#C96868"))
        all_blocks.append(canvas.create_rectangle((x1, 150), (x2, 180), fill="#FADFA1"))
        all_blocks.append(canvas.create_rectangle((x1, 230), (x2, 260), fill="#557C56"))
        x1 += 80
        x2 += 80
    # Even rows of blocks
    x21 = 35
    x22 = 105
    for i in range(8):
        all_blocks.append(canvas.create_rectangle((x21, 110), (x22, 140), fill="#7EACB5"))
        all_blocks.append(canvas.create_rectangle((x21, 190), (x22, 220), fill="#FF885B"))
        x21 += 80
        x22 += 80


def move_to_right(event):
    if canvas.coords(paddle)[2] < 710:
        canvas.move(paddle, 20, 0)


def move_to_left(event):
    if canvas.coords(paddle)[0] > -10:
        canvas.move(paddle, -20, 0)


def moving_ball():
    global x_speed, y_speed, score, highscore, reset_btn, game_over_label, winning_label
    timer = window.after(20, moving_ball)
    canvas.move(ball, x_speed, y_speed)
    # Hitting the left and right walls
    if canvas.coords(ball)[0] > 690 or canvas.coords(ball)[0] < -8:
        x_speed *= -1
    # Hitting the sky
    if canvas.coords(ball)[1] < 60:
        y_speed *= -1
    # Losing the game
    if canvas.coords(ball)[1] > 490:
        canvas.create_window(350, 250, window=game_over_label)
        # Storing the highscore.txt
        with open("highscore.txt", "r") as read_file:
            old_highscore = int(read_file.read())
        if old_highscore < score:
            with open("highscore.txt", "w") as write_file:
                highscore = score
                highscore_label.config(text=highscore)
                write_file.write(str(highscore))
        # Making the reset btn
        canvas.create_window(350, 350, window=reset_btn)
        window.after_cancel(timer)
    #  Hitting the paddle
    if (canvas.coords(ball)[0] <= canvas.coords(paddle)[2] and
            canvas.coords(ball)[1] <= canvas.coords(paddle)[3] and
            canvas.coords(ball)[2] >= canvas.coords(paddle)[0] and
            canvas.coords(ball)[3] >= canvas.coords(paddle)[1]):
        y_speed *= -1
        if x_speed > 0:
            x_speed += 0.25
        else:
            x_speed -= 0.25
        if y_speed > 0:
            y_speed += 0.25
        else:
            y_speed -= 0.25
    #  Hitting the blocks
    if not all_blocks == []:
        for i in all_blocks:
            if (canvas.coords(ball)[0] <= canvas.coords(i)[2] and
                    canvas.coords(ball)[1] <= canvas.coords(i)[3] and
                    canvas.coords(ball)[2] >= canvas.coords(i)[0] and
                    canvas.coords(ball)[3] >= canvas.coords(i)[1]):
                canvas.delete(i)
                all_blocks.remove(i)
                score += 1
                score_label.config(text=score)
                y_speed *= -1
    else:
        canvas.create_window(350, 250, window=winning_label)
        # Adding the highscore.txt
        highscore = score
        highscore_label.config(text=highscore)
        # Storing the highscore.txt
        with open("highscore.txt", "w") as file2:
            file2.write(str(highscore))
        # Making the reset btn
        reset_btn = Button(text="Reset", fg="green", bg="#D6CFB4", font=("Roboto", 15, "bold"), command=reset)
        canvas.create_window(350, 350, window=reset_btn)
        window.after_cancel(timer)


def reset():
    global x_speed, y_speed, score, all_blocks, reset_btn, winning_label, game_over_label
    x_speed = 5
    y_speed = -5
    score = 0
    score_label.config(text="0")
    canvas.coords(ball, 370, 460, 390, 480)
    for item in all_blocks:
        canvas.delete(item)
        all_blocks.remove(item)
    making_blocks()
    reset_btn.destroy()
    game_over_label.destroy()
    winning_label.destroy()
    game_over_label = Label(text="Game Over", font=("Roboto", 40, "bold"), fg="white", bg="black")
    winning_label = Label(text="You have Won!!", font=("Roboto", 40, "bold"), fg="red", bg="black")
    reset_btn = Button(text="Reset", fg="green", bg="#D6CFB4", font=("Roboto", 15, "bold"), command=reset)
    moving_ball()


# Making the canvas
canvas = Canvas(height=500, width=700, bg="black")
canvas.grid(column=0, row=0)
# Making the score labels
score_label = Label(text="0", fg="white", font=("Roboto", 30, "normal"), bg="black")
canvas.create_window(70, 40, window=score_label)
# Reading the highscore
with open("highscore.txt") as file:
    highscore_text = file.read()
    highscore_label = Label(text=highscore_text, font=("Roboto", 30, "normal"), fg="white", bg="black")
    canvas.create_window(630, 40, window=highscore_label)
# Making the blocks
making_blocks()
# Making the paddle
paddle = canvas.create_rectangle((300, 485), (390, 500), fill="#F5F5F5")
window.bind("<Right>", move_to_right)
window.bind("<Left>", move_to_left)
# Creating the ball
ball = canvas.create_oval((370, 460), (390, 480), fill="white", disabledoutline="")
# Making the functionality of the ball
moving_ball()
# Making the reset btn
reset_btn = Button(text="Reset", fg="green", bg="#D6CFB4", font=("Roboto", 15, "bold"), command=reset)
# Making the game over and win labels
game_over_label = Label(text="Game Over", font=("Roboto", 40, "bold"), fg="white", bg="black")
winning_label = Label(text="You have Won!!", font=("Roboto", 40, "bold"), fg="red", bg="black")
window.mainloop()
