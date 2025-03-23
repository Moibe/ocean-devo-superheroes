firebase.initializeApp(firebaseConfig);
// Provider de Google
const provider = new firebase.auth.GoogleAuthProvider();


// Listener para detectar el estado de autenticación
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // El usuario ha iniciado sesión
        //updateUI(user);

        // El usuario ha iniciado sesión
        console.log("Usuario autenticado:", user.uid);

        // Redirigir a hola.html
        //window.location.href = "hola.html";
    } else {
        // El usuario ha cerrado sesión o no ha iniciado sesión
        //updateUI(null);
        console.log("Usuario no autenticado:");
    }
});