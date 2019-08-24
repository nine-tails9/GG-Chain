new Vue({
    delimiters : ['[[',']]'],
    el: '#app',
    data: {
        name: "SS",
        model : ''
    },
    methods: {
        async start_download() {
            let modelLoad = await fetch('/download_dataset')
                .then(function (response) {
                    return response.json();
                })
                .then(function (myJson) {
                    // console.log(JSON.stringify(myJson));
                    return myJson;
                });
            console.log(modelLoad);
            const model = await tf.loadLayersModel("http://127.0.0.1:5000/static/model/model.json");
            // console.log(model);
            await model.save('indexeddb://my-model');
        },
        handleModel(){
            this.file = this.$refs.model.files[0];
        }
    }
});
