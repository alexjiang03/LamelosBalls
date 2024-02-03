foreach filename [glob -nocomplain -types f -- ./playerData/*] {
    set info [exec cat $filename]

    set info "GAME,$info"; # Add GAME header to start of table

    # Split the table into lines
    set lines [split $info "\n"]

    # Populate the "GAME" column with incremental numbers starting from 0
    for {set i 0} {$i < [llength $lines]} {incr i} {
        if {$i > 0} {
            set lines [lreplace $lines $i $i "[expr $i-1],[lindex $lines $i]"]
        }
    }

    # Join the lines back into a table
    set info [join $lines "\n"]
    
    set f [open $filename w]
    puts $f $info
    close $f
}