document.getElementById('download').addEventListener('click', () =>{
    setTimeout(download_video, 2000);
});

async function download_video(){
    await fetch('/facetube/facebook/get').then(res => {
        console.log(res)
        if (res.status == 404){
            return download_video()
        }
        if (res.status == 200){
            let download = document.createElement('a');

            download.style.display = 'none';
            res.json().then(data =>{
                download.setAttribute('href', data.url);
                download.setAttribute('download', data.name);
                document.body.appendChild(download);
                download.click();
            });
        }
    });
}