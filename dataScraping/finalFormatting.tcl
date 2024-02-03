foreach filename [glob -nocomplain -types f -- ./playerData/*] {
    set info [exec cat $filename]

    # Remove vs. or @ from start of opponent columns
    regsub -all {(vs\.[^A-Z]*)|(\@ )} $info {} info

    set info "GAME,$info"; # Add GAME header to start of table

    set lines [split $info "\n"]; # Split the table into lines

    # Populate the "GAME" column with incremental numbers starting from 0
    for {set i 0} {$i < [llength $lines]} {incr i} {
        if {$i > 0} {
            set lines [lreplace $lines $i $i "[expr $i-1],[lindex $lines $i]"]
        }
    }

    set info [join $lines "\n"]; # Join the lines back into a table
    
    # Overwrite player data file
    set f [open $filename w]
    puts $f $info
    close $f

    puts "Completed final data formatting on $filename"
}

puts "Done"

# Run this from /dataScraping/ afterwards to make sure all's good :)
# find ./playerData -type f -exec sh -c 'test "$(wc -l < "$1")" -gt 12' sh {} \; -print