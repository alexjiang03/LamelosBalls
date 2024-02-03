# This script:
#   - Removes the vs. and @ from the start of the opponent column
#     to simplify later adding opponent stats in
#   - Adds a game number to each row
#   - Creates a single, large .csv file with all of the players
#     data in it, with an additional label of "PLAYER"

# Setup & open the larger, combined db file
set allPlayersFile [open "./allPlayers.csv" w]
puts $allPlayersFile "PLAYER,GAME,OPP,MIN,REB,AST,TO,STL,BLK,PF,PTS"

foreach filename [glob -nocomplain -types f -- ./playerData/*] {
    set info [exec cat $filename]

    # Remove vs. or @ from start of opponent columns
    regsub -all {(vs\.[^A-Z]*)|(\@ )} $info {} info

    set info "GAME,$info"; # Add GAME header to start of table

    set lines [split $info "\n"]; # Split the table into lines

    # Get playername from filename-.csv
    set pname ""
    regexp {playerData/([^\.]+)\.csv} $filename _temp pname

    for {set i 1} {$i < [llength $lines]} {incr i} {
        set lines [lreplace $lines $i $i "[expr $i-1],[lindex $lines $i]"]; # Populate the "GAME" column with incremental numbers starting from 0
        puts $allPlayersFile "$pname,[lindex $lines $i]"; # Add player name to & print to combo file
    }

    set info [join $lines "\n"]; # Join the lines back into a table
    
    # Overwrite player data file
    set f [open $filename w]
    puts $f $info
    close $f

    puts "Completed final data formatting on $filename"
}

close $allPlayersFile

puts "Done"

# Run this from /dataScraping/ afterwards to make sure all's good (should return nothing)
# find ./playerData -type f -exec sh -c 'test "$(wc -l < "$1")" -gt 12' sh {} \; -print