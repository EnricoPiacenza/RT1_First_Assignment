### Define libraries, modules and global variables needed for the correct functioning of the program

1. Import libraries and modules.

2. Global variables:
   - `a_th`(float): Threshold for the control of the orientation.
   - `d_th`(float): Threshold for the control of the linear distance.
   - `d_dh`(float): Threshold for the control of the distance we want to drop the collected token from the target one.
   - `rot_direction`(integer): Threshold to control the sense of rotation of the robot to find the next token.
   - `tokens_grabbed`(list): List to store the tokens already collected. 
   - `target_token`(integer): Code of the token used as a reference to collect the others. 
   - `next_to_grab`(integer): Code of the next nearest token to grab and collect.

3. Initialize the Robot object (`R`).

### Pseudocode of function main()

1. Function `main`:
   - Record the starting time (`t_0`).
   - Call `def_target_token()` to compute the target token.
   - Call `def_collecting_area()` to define the collecting area.
   - Call `grab_all_tokens()` to collect all tokens and bring them in the collecting area.
   - Record the ending time (`t_1`).
   - Print the time necessary to collect all tokens: `t_1 - t_0` in seconds.

### Pseudocode of the functions called in main()    

1. Function `def_target_token()`:
   - Call `find_nearest()` to determine the closest token to the robot.
   - If the global variable `next_to_grab` is `-1`:
      - Print "Error, no token detected".
      - Terminate the program.
   - Call `reach_token(next_to_grab, d_th)` to reach the target token.
   - Call the robot function `R.grab()` to grab the token.
   - Append `next_to_grab` to the global list `tokens_grabbed`.
   - Set `target_token` to `next_to_grab`.
   - Print "Target token: {target_token}".

2. Function `def_collecting_area()`:   
   - Call `find_furthest()` to find the furthest token from the robot.
   - Save the returned value in the local variable `dist`.
      - If `dist` is equal to `-1`:
         - Print `All tokens were collected`.
         - Call the robot function `R.release()`.
         - Terminate the program.
   - Call the ausiliar function `reach_token(next_to_grab, dist/2)` to position the robot halfway between the target token and the furthest token.
   - Call the robot function `R.release()` to release the token.
   - Call the robot function `drive(-30,1)` to drive backwards and correctly position to search for the next token.

3. Function `grab_all_tokens()`:
   - Start an infinite loop:
      - Call `find_nearest()` to find the nearest token, the code of it will be saved in the global variable `next_to_grab`.
      - If `next_to_grab` is equal to `-1`:
         - Print "All tokens were collected".
         - Break the loop.
      - Call `collect_nearest()` to collect the nearest token.
      - Call `bring_back_nearest()` to bring back the collected token in the collecting area.
      - Print "Tokens collected: {tokens_grabbed}".

### Pseudocode of the ausilary functions

1. Function `reach_token(code, dist)`:
   - Start an infinite loop:
   - Call the function `find_token(next_to_grab)` and save the returned values:
      - `d`, the distance from the token we want to reach.
      - `angl`, the angle between the robot and the desired token.
   - If `d` is equal to `-1` or `angl` is equal to `-1`:
      - Call the robot function `turn(rot_direction*40,0.1)` to turn the robot for 0.1 seconds (rot_direction specify the sense of rotation).
   - If `d` is less than `dist`:
      - Return.
   - If `angl` is greater than `a_th`:
      - Call the robot function `turn(5,0.1)` to correctly align the robot with the desired token.
   - If `angl` is less than -`a_th`:
      - Call the robot function `turn(5,0.1)` to correctly align the robot with the desired token.
   - Else:
      - Call the robot function `drive(50,0.1)` to drive towards the desired token as the robot is aligned with it.

2. Function `find_nearest()`:
   - Initialize `dist` equal to 100.
   - Inizialize `code` equal to 0.
   - Initialize `ideal` to "clockwise".
   - Initialize `t_0` with the current time.
   - Print "Searching for the nearest token..."
   - Start a loop:
      - Call the robot function `turn(40,0.1)` to look for tokens.
      - Start a for loop to scan all tokens present in the list `R.see()`:
         - If `token.dist` is less than `dist` and `token.info.code` is not in the global list `tokens_grabbed`:
            - Update `dist` with "token.dist".
            - Update `code` with "token.info.code".
            - Calculate the current time and save the it in `t_t`.
            - If `t_t - t_0` is less than 1.6 seconds:
               - Set `rot_direction` to 1.
            - Else:
               - Set `rot_direction` to -1.
               - Update `ideal` to "counterclockwise".
      - Calculate the current time and save it in `t_1`.
      - If `t_1 - t_0` is greater than or equal to 3.15:
         - Break the loop.
   - If `dist` is equal to 100:
      - Set the global variable `next_to_grab` to -1.
   - Else:
      - set the global variable `next_to_grab` equal to `code`.
   - print "--> Token code: {code}, dist: {dist}, Most efficient sense of rotation: {ideal}".

3. Function `find_furthest()`:
   - Initialize `dist` equal to 0.
   - Inizialize `code` equal to 0.
   - Initialize `ideal` to "clockwise".
   - Initialize `t_0` with the current time.
   - Print "Searching for the furthest token..."
   - Start a loop:
      - Call the robot function `turn(40,0.1)` to look for tokens.
      - Start a for loop to scan all tokens present in the list `R.see()`:
         - If `token.dist` is greater than `dist` and `token.info.code` is not in the global list `tokens_grabbed`:
            - Update `dist` with "token.dist".
            - Update `code` with "token.info.code".
            - Calculate the current time and save the it in `t_t`.
            - If `t_t - t_0` is less than 1.6 seconds:
               - Set `rot_direction` to 1.
            - Else:
               - Set `rot_direction` to -1.
               - Update `ideal` to "counterclockwise".
      - Calculate the current time and save it in `t_1`.
      - If `t_1 - t_0` is greater than or equal to 3.15:
         - Break the loop.
   - If `dist` is equal to 0:
      - Set the global variable `next_to_grab` to -1.
   - Else:
      - set the global variable `next_to_grab` equal to `code`.
   - print "--> Token code: {code}, dist: {dist}, Most efficient sense of rotation: {ideal} ".

4. Function `collect_nearest()`:
   - Call the ausilary function `reach_token(next_to_grab, d_th)`.
   - If `R.grab()` returns `True`:
      - Print "token: {next_to_grab} grabbed successfully."

5. Function `bring_back_nearest()`:
   - Invert the global variable `rot_direction`.
   - Call `reach_token(target_token, d_dh)`.
   - If `R.grab()` returns `True`:
      - Print "token: {next_to_grab} grabbed successfully."
      - Call the robot function `Drive(-30,1)` to drive backwards and correctly position to search for the next token. 

### Pseudocode of the robot functions

1. Function `drive(speed, seconds)`:
   - Set the power of motors `m1` and `m2` equal to `speed`.
   - Sleep for `seconds`.
   - Set the power of motors `m1` and `m2` equal to 0 to stop the robot.

2. Function `turn(speed, seconds)`:
   - Set the power of the `m1` equal to `speed`.
   - Set the power of the `m2` equal to `-speed`.
   - Sleep for `seconds`.
   - Set the power of motors `m1` and `m2` equal to 0 to stop turning.

3. Function `find_token(code)`:
   - Initialize `dist` equal to 100.
   - Start a for loop to scan all tokens present in the list `R.see()`:
      - If `token.info.code` is equal to`code`:
         - Set dist equal to token.dist.
         - Set rot_y equal to token.angl.
         - Break the loop.
   - If `dist` equal to 100: return -1 for distance and -1 for angle.
      - Return dist equal to -1.
      - Return rot_y equal to -1.
   - Else:
      - Return dist.
      - Return rot_y.