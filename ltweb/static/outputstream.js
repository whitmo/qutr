var viz;
viz.data = {};
var blocker;

$(document).ready(function() {
    var socket = io.connect('/jobs'); // disambiguate channelname and api endpoint?
    socket.emit('subscribe', {job_id:job_id});
    var outputLine = $$(
        {
            model:{},
            view:{
                format: $('#lineformat').html()
            },
            controller: {}
        }),
        visual = $$({url:null}, {format:"#visual_layout"}, {}),
        outputStream = $$(
        {
            model:{id: job_id, lines:null},
            view:{
                format:$("#streamformat").html()
            },
            controller:{
                'persist:loads:success': function(){
                    var stream = this;
                    $.each(this.model.get().lines, this.addLine);
                },
                'create': function(){
                    this.persist($$.adapter.restful, {collection:'jobs'});
                    this.load();
                    var stream = this;

                    this.addLine = function(e){
                        var newLine = $$(outputLine, {content: e});
                        stream.append(newLine, 'ul');
                        var el = newLine.view.$();
                        $('html, body').animate({
                            scrollTop: el.offset().top
                        }, 200);
                    };

                    this.handleData = function(e){
                        console.log(e);
                        viz.data = e;
                    };

                    this.load = function(e){
                        if (e.type === 'viz'){
                            console.log(e);
                            var newviz = $$(visual, {url:e.url});
                            stream.append(newviz);
                        }

                    };
                    socket.on("load", this.load);
                    socket.on("stop", this.stop);
                    socket.on("lineOut", this.addLine);
                    socket.on("dataOut", this.handleData);
                }
            }
        });

    $$.document.append(outputStream);
});