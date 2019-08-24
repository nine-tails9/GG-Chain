
async function start_download() {
    let modelLoad = await fetch('/download_dataset')
        .then(function(response) {
            return response.json();
        })
        .then(function(myJson) {
            // console.log(JSON.stringify(myJson));
            return myJson;
        });
    // console.log(modelLoad)
    const model = await tf.loadLayersModel(modelLoad);
}
