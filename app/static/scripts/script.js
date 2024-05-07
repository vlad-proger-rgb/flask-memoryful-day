function monthNumberToMonthName(num) {
    let monthNames = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ];

    if (num >= 1 && num <= 12) {
        return monthNames[num - 1];
    } else {
        return "Invalid month number";
    }
}

function getDateOneMonthAgo() {
    let today = new Date();
    let oneMonthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    return oneMonthAgo.toISOString().split('T')[0]; // Format: YYYY-MM-DD
}