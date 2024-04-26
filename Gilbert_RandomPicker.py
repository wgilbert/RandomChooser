"""
Gilbert_RandomPicker

Description:
"""
####imports and variable setup####
import random
import tsapp

choosing_class = True
chosen_period = 0
files = ["first.txt", "second.txt", "third.txt", "fifth.txt", "sixth.txt", "seventh.txt"]
eaton_green = (118, 190, 67)
eaton_blue = (14, 35, 62)
title_size = 100
choices = []
drums = tsapp.Sound("Drumroll.mp3", unique = True, looping = False)
crash = tsapp.Sound("Drum3.mp3", unique = True, looping = False)

#### Function Definitions ####
def load_class(filename):
    """ a function that reads a text file and processes the contents into a list
    
    PARAMETER:
    ----------
    filename(string): the file name that contains zero or more lines of information
                      to process
                      
    RETURN:
    -------
    list:  returns a list of the contents of the file.  each list item is stripped of any
           white space or special characters at the beginning or the end
    """
    
    with open(filename) as file:
        class_list = file.readlines()
        for i in range(len(class_list)-1, -1,-1):
            if class_list[i].isspace():
                del(class_list[i])
            else:
                class_list[i] = class_list[i].strip(".,-;!@#$%^&* ")
    return class_list
                
                    
def get_next(choices_list):
    """ a function that gets a random choice from a list and then removes the choice from that list
    
    PARAMETER:
    ----------
    choices_list(list): the list from which to choose a random item.  The item chosen will be removed
                        from the list as a function side-effect
                      
    RETURN:
    -------
    choice:  the item chosen from and removed from the list.
    """

    choice = None
    if len(choices_list) > 0:
        choice = random.choice(choices_list)
        choices_list.remove(choice)
    return choice


####Create Graphics for Background and Title####

window = tsapp.GraphicsWindow(1920, 1080, eaton_green)
title = tsapp.TextLabel("Acme-Regular.ttf", title_size, 0, int(title_size*.9), window.width, "You Have Been Chosen!", eaton_blue)
title.align = "center"
window.add_object(title)

####draw buttons####
button_files = ["Numpad1.png", "Numpad2.png", "Numpad3.png", "Numpad5.png", "Numpad6.png", "Numpad7.png"]
buttons = []
class_periods = [1,2,4,5,6,7]
button_width = 80
y = title.y + .5*title_size

## the offset is the space between each button.
## it is calculated as 10% of the free space remaining after subracting the total width of all buttons from the window
offset = int(.1* (window.width - (len(button_files) * button_width)))

"""
buttons are positioned using a linear algebraic function y = mx + b 
where m is the width of the button plus the offset between buttons
x will be the index number from the loop reperesented as 'i' here
b is the starting x position of the first button calculated by first multiplying the number of buttons
by the width of all the buttons and all the offsets, subtracting that from the window width and dividing in half
"""
start_x = window.width - (len(button_files) * button_width) - ((len(button_files) - 1) * offset)
start_x = int(start_x / 2)


for i in range(len(button_files)):
    x = start_x + i*(button_width + offset)
    temp = tsapp.Sprite(button_files[i], x, y)
    buttons.append(temp)
    window.add_object(temp)



####Name Choice text setup####
##The name text label is dynamically positioned to appear below the program title
y = title.y + 1.5*title_size
name_label = tsapp.TextLabel("Acme-Regular.ttf", title_size, 0, y, window.width, "Click Next Icon to Start", eaton_blue)
name_label.align = "center"
window.add_object(name_label)
name_label.visible = False

##The next double arrow icon is dynamically positioned to appear below the name text label and horizontally centered on the screen
next_icon = tsapp.Sprite("IconDoubleArrow.png", 0, 0)
next_icon.scale = .75
next_icon.center_x = window.center_x
next_icon.y = name_label.y + title_size
window.add_object(next_icon)
next_icon.visible = False

##The next save icon is dynamically positioned to appear at the lower right edge of the screen
save_icon = tsapp.Sprite("EditIcon.png", 0, 0)
save_icon.x = window.width - save_icon.width - 20
save_icon.y = window.height - save_icon.height - 20
window.add_object(save_icon)
save_icon.visible = False

##The reset icon is dynamically positioned to appear at the lower left edge of the screen
reset_icon = tsapp.Sprite("IconReset.png", 0, 0)
reset_icon.x = 20
reset_icon.y = window.height - reset_icon.height - 20
window.add_object(reset_icon)
reset_icon.visible = False
## all of the above icons are set to be initially invisible.  The main graphics loop will show them
## at the appropriate time

#### Main program control loop will continue until the user presses the red x to close the window
while window.is_running:
    ### This section will run when the user has not yet chosen a class period
    if choosing_class:
        ##hide all unnecessary icons
        next_icon.visible = False
        save_icon.visible = False
        name_label.visible = False

        window.finish_frame()
        ##check for a mouse press during this frame and store the position
        if tsapp.was_mouse_pressed():
            mouse_x, mouse_y = tsapp.get_mouse_position()
            
            #Determine which button was clicked and store the index of the chosen period
            for i in range(len(buttons)):
                if buttons[i].is_colliding_point(mouse_x, mouse_y):
                    chosen_period = i
                    choosing_class = False
            if not choosing_class:
                for button in buttons:
                    button.visible = False
                window.finish_frame()
    

        ##read the file for the chosen class period
        choices = load_class(files[chosen_period])
    
    
    ###Class is chosen, this section begins name selection for the chosen class
    if not choosing_class:
        ##show necessary icons
        next_icon.visible = True
        save_icon.visible = True
        name_label.visible = True
        window.finish_frame()
        
        ##check for a mouse press during this frame and store the position
        if tsapp.was_mouse_pressed():
            mouse_x, mouse_y = tsapp.get_mouse_position()
            #if the next icon is selected, use the get_next function to get a name
            #and update the name_label text property
            if next_icon.is_colliding_point(mouse_x, mouse_y):
                student = get_next(choices)
                if student != None:
                    name_label.text = student
                    drums.play()
                    while drums.get_num_copies() > 0:
                        pass
                    crash.play()
                    window.finish_frame()
                else:
                    name_label.text = "All Students Have Been Chosen"
            #if the save icon is selected, update the contents of the .txt file with what
            #is remaining of the choices list.  Hide appropriate icons and show the reset icon
            elif save_icon.is_colliding_point(mouse_x, mouse_y):
                with open(files[chosen_period], "w") as file:
                    print(*choices, sep="", file = file)
                next_icon.visible = False
                save_icon.visible = False
                name_label.visible = False
                reset_icon.visible = True
                window.finish_frame()

    ### This section occurs when the file has been saved and gives the user a chance to reset and go back to class selection    
    if reset_icon.visible:
        ##check for a mouse press during this frame and store the position
        if tsapp.was_mouse_pressed():
            mouse_x, mouse_y = tsapp.get_mouse_position()
            #changes the choosing_class boolean back to true, hides unecessary icons, and shows the buttons again
            if reset_icon.is_colliding_point(mouse_x, mouse_y):
                reset_icon.visible = False
                choosing_class = True
                for button in buttons:
                    button.visible = True
                    
                window.finish_frame()
            
            
        