$(document).ready(function() {
    var socket;
    var outputLine = $$(
        {
            model:{},
            view:{
                format: $('#lineformat').html()
            },
            controller: {}
        });

    var outputStream = $$(
        {
            model:{id: job_id},
            view:{
                format:$("#streamformat").html()
            },
            controller:{
                'create': function(){
                    this.persist($$.adapter.restful, {collection:'jobs'});
                    this.load();
                    socket = io.connect('/jobs');
                    socket.emit('subscribe', {job_id:job_id});
                    var stream = this;
                    socket.on("jobOut",
                              function(e){
                                  var newLine = $$(outputLine, {content:e});
                                  stream.append(newLine, 'ul');
                              });
                }
            }
        });

    $$.document.append(outputStream);
});