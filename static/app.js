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
            var reader = new FileReader();
            reader.readAsText(this.shards[0]);
            reader.onload = this.loaded;

        },
        loaded(item){
            this.loading.model = true;
            fetch('/new_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: item['currentTarget']['result']

            })
                .then(res => {
                    this.loading.model = false;
                    console.log(res)
                })
        }
    }
});
