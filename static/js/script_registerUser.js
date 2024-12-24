const userType = document.getElementById('userType');
const commonFields = document.getElementById('commonFields');
const corporateFields = document.getElementById('corporateFields');

userType.addEventListener('change', function () {
    if (this.value === 'comun') {
        commonFields.style.display = 'block';
        corporateFields.style.display = 'none';
    } else if (this.value === 'corporativo') {
        commonFields.style.display = 'none';
        corporateFields.style.display = 'block';
    } else {
        commonFields.style.display = 'none';
        corporateFields.style.display = 'none';
    }
});