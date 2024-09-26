var age = 23
var prova = 9
fun main() {

    // Check if the age is a valid number
    /* trial * "" /* /
    / comment */
    /**/ /*
    */
    if(age > 0){

        println("Hello, user!")         // Print a message

        // Example of a simple condition
        if (age >= 18) {
            println("You are an adult.")
            age = 0
            prova = 20
            println(prova)
        } else {
            println("You are not an adult yet.")
            println(age)
        }
        if (age <= 6) {
            println(prova)
            println("You are a baby.")
        }
        if (age == 100) {
            println("WoW, you are OLD")
        }
        if (age > 100) {
            println("WoW, you are dead")
        }
        for (i in 2 .. 15 step 3) {
            println(i)
        }
    } else {
        println("Invalid age entered.")
    }

    // Ask for the user's name
    println("Enter your name: ")
    val name = readLine()
    println(name)
}
