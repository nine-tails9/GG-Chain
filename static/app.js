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
            let dataset = await fetch('/download_dataset')
                .then(function(response) {
                    return response.json();
                })
                .then(function(myJson) {
                    // console.log(JSON.stringify(myJson));
                    return myJson;
                });
            let xtrain = tf.tensor(eval(dataset['train']['x']));
            let ytrain = tf.tensor(eval(dataset['train']['y']));
            let xtest = tf.tensor(eval(dataset['test']['x']));
            let ytest = tf.tensor(eval(dataset['test']['y']));

            let model = await tf.loadLayersModel("http://127.0.0.1:5000/static/model/model.json");
            await model.save('indexeddb://my-model');

            let updatedShards = await fetch('/last_block')
                .then(function(response) {
                    return response.json();
                })
                .then(function(myjson) {
                    return myjson;
                });

            // console.log(model.summary());
            model.compile({
                optimizer: 'adam',
                loss: 'categoricalCrossentropy',
                metrics: ['accuracy']
            });

            function onBatchEnd(batch, logs) {
                console.log('Accuracy', logs.acc);
            }
            // tf.tensor(dataset['train']['x']).print()
            model.fit(xtrain, ytrain)
                .then(info => {
                    console.log('Final accuracy', info.history.acc);
                });
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
            reader.onload = this.loaded();

        },
        loaded(item, fileList){

            this.loading.model = true;
            let model = {'file': this.shards[0], 'data': item['currentTarget']['result']}
            fetch('/new_model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: model

            })
                .then(res => {
                    this.loading.model = false;
                    console.log(res)
                })
        }
    }
});
