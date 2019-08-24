new Vue({
    delimiters : ['[[',']]'],
    el: '#app',
    data: {
        name: "SS",
        model : '',
        shards: [],
        err: false,
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
            this.model = this.$refs.model.files[0];
        },
        handleShards(){
            this.shards = this.$refs.shard.files;
            console.log(this.shards);
        },
        uploadModel(){

            if(!this.model || this.shards.length === 0){
                this.err = true;
                return;
            }
            this.loading.model = true;

            this.err =  false;
            let formData = new FormData();
            formData.append('model', this.model);

            for(let i = 0; i < this.shards.length; i++)
                formData.append('shards' + i, this.shards[i]);

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
