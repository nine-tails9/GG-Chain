new Vue({
    delimiters : ['[[',']]'],
    el: '#app',
    data: {
        name: "SS",
        model : '',
        file: '',
        loading: {
            model: false,
            shard: false
        }
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
            await model.save('indexeddb://my-model');
        },
        handleModel(){
            this.file = this.$refs.model.files[0];
        },
        uploadModel(){
            this.loading.model = true;
            let formData = new FormData();
            formData.append('file', this.file);

            fetch('/new_model', {
                method: 'POST',
                headers: {
                    "Content-Type": "multipart/form-data"
                },
                body: formData

            })
                .then(res => {
                    this.loading.model = false;
                    console.log(res)
                })
        },
    }
});
