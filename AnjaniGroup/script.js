function calculatePremium() {
    var age = parseInt(document.getElementById('age').value);
    var coverageAmount = parseInt(document.getElementById('coverageAmount').value);
    var term = parseInt(document.getElementById('term').value);

    // Basic premium calculation logic
    var basePremium = coverageAmount * age * term / 1000;

    // Additional logic can be added for more accurate premium calculation based on factors like health, occupation, etc.

    var premiumResult = document.getElementById('premiumResult');
    premiumResult.innerHTML = "Your life insurance premium is: ₹" + basePremium.toFixed(2);
}
