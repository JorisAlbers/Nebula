var farFetched = function (cursusName, config) {
  const domain = 'api.php';

  if (config.max) {
    set = '&set=' + config.max;
  }
  fetch(domain + '?cursus=' + cursusName + set)
    .then(function (response) {
      return response.json()
    })
    .then(function (cursus) {

      document.getElementById('spots--taken')
        .innerHTML = cursus.inschrijvingen;
      document.getElementById('spots--total')
        .innerHTML = cursus.maxInschrijvingen;

      document.getElementById('signupForm')
        .action = domain + '?cursus=' + cursusName;

      if (cursus.inschrijvingen >= cursus.maxInschrijvingen) {
        var el = document.getElementById('inschrijven');
        el.className += ' cursus--full';

      }
    })
    .catch(function (ex) {
      console.log('parsing failed', ex)
    })
}

var farSend = function (evt) {
  evt.preventDefault();
}
