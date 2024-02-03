set allPlayersFile [open "./playerData/allPlayers.csv" w]
puts $allPlayersFile "PLAYER,GAME,OPP,MIN,REB,AST,TO,STL,BLK,PF,PTS"

foreach filename [glob -nocomplain -types f -- ./playerData/*] {
    set info [exec cat $filename]
    set lines [split $info "\n"]; # Split the table into lines
    set pname ""
    regexp {playerData/([^\.]+)\.csv} $filename _temp pname

    # Populate the "GAME" column with incremental numbers starting from 0
    for {set i 1} {$i < [llength $lines]} {incr i} {
        puts $allPlayersFile "$pname,[lindex $lines $i]"
    }

    puts "Merged $filename to playerData/allPlayers.csv"
}

close $allPlayersFile
puts "Done"