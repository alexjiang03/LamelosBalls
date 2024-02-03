set allPlayersFile [open "./allPlayers.csv" w]
puts $allPlayersFile "PLAYER,GAME,MIN,REB,AST,TO,STL,BLK,PF,PTS,W,L,Diff,OFFENSE: Pts/Poss,OFFENSE: eFG%,OFFENSE: TOV%,OFFENSE: ORB%,OFFENSE: FT Rate,DEFENSE: Pts/Poss,DEFENSE: eFG%,DEFENSE: TOV%,DEFENSE: ORB%,DEFENSE: FT Rate"

foreach filename [glob -nocomplain -types f -- ./playerData/*] {
    set info [exec cat $filename]
    set lines [split $info "\n"]; # Split the table into lines
    set pname ""
    regexp {playerData/([^\.]+)\.csv} $filename _temp pname

    # Populate the "GAME" column with incremental numbers starting from 0
    for {set i 1} {$i < [llength $lines]} {incr i} {
        # Convert percentages to decimal
        set statline [lindex $lines $i]
        regsub -all {,([\d]*)\.([\d]*)\%} $statline {,0.\1\2} statline

        # Print to file
        puts $allPlayersFile "$pname,$statline"
    }

    puts "Merged $filename to playerData/allPlayers.csv"
}

close $allPlayersFile
puts "Done"