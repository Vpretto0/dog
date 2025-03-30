# THE DOG EXPERIENCE
### ROBOT DOG UI and Backend

Project For CoD PRCTM.


## Content:

 - **UI:**
     - **[Main Menu](start_menu.py):**
         - **[Database UI](law_and_order.py):**
             - **[Barcode Scanner](bar_code.py):**
                 - **[Barcode Image](barcode.png):** Kind of Cache for the Barcode
                 - **[Print](click_here.py):** Print Function
                     - **[Main Canva](print_ident_color.py):** Main Canva
                     - **[Print Cache(?)](canvas.png):** Other Kind of Cache more
             - **[Profile Picture](photo.py):** Student, Staff or Guest Picture
                 - **[The Photo](photo.png):** Other Kind of Cache, but for the image
         - **[Tracking](verification_tracking.py):** Main Verification database UI (Not Finished yet)   :(
             - **[Robot Cameras](robot_tracking):** main file thathandling the 5.5 basic robot cameras
             - **[Maps](maps.py):** maps availables to localize the robot
             - **[Emergency STOP](estop.py):** emergency buton to stop the robot in emergency
             - **[Manual/Auto swich](manual_mode.py):** Manual/Auto Switch
 - **DATABASEs:**
     - **[Main Database](db_identity.py):** Database for Users
     - **[Verification Database](db_identity_verification.py):** Verification Records 
 - **Raspberry:**
     - **[Raspberry Backend](raspi_exe.py):** For verification in the Raspberry
     - **[Arduino Main Code](rastpi_to_arduino.ino):** Arduino Main Code
         - **[Basic Vz of the Arduino Main Code](rastpi-basic_complete.ino):** basic Version
         - **[Checking Speaker](bocina.ino):** checking it works (because it didn’t work)
 - **Other Images:**
     - **[School Logo](images/BHS.png) (Main size)**
     - **[School Logo](images/BHS(32px).png )(32px)**
     - **[School Logo](images/BHS(40px).png) (40px)**
     - **[School Logo](images/BHS(44px).png) (44px)**
     - **[Something](images/boring_text.png)**
     - **[Info](images/info-24.png) (?)**
     - **[Police Dog](images/police_dog002.jpg)**
     - **[Print Icon](images/printer-24.png)**
     - **[Siren](images/siren.gif)**

## Errors:
 - **Error in:** [Main Menu](start_menu.py), Because I don't code the go back part, you cannot go back
 - **Database bug:** [Database](law_and_order.py) When you add an user and try Display to show the new user (I'm not gonna fix it, because I'm lazy)

