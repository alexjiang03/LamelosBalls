foreach filename [glob -nocomplain -types f -- ./playerData/*] {
    set info [exec cat $filename]
    regsub -all {(vs\.[^A-Z]*)|(\@ )} $info "" info
    
    set f [open $filename w]
    puts $f $info
    close $f
}