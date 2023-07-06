export default class APIService {

    static SendDetails(body) {
        return fetch('http://127.0.0.1:5000/sendEmails/', {
            'method': "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .catch(error => console.log(error))
    }

}