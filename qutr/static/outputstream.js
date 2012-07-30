var viz = {};
viz.data = {};

var blocker;

$(document).ready(function() {
    var socket = io.connect('/jobs'); // disambiguate channelname and api endpoint?
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
                'persist:load:success': function(){
                    var stream = this;
                    var lines = this.model.get().lines;
                    //console.log(lines.pop());
                    $.each(lines, function(index, value){stream.addLine(value);});
                },

                'create': function(){
                    socket.emit('subscribe', {job_id:job_id});
                    this.persist($$.adapter.restful, {collection:'jobs'});
                    this.load();
                    var stream = this;

                    this.addLine = function(line){
                        var newLine = $$(outputLine, {content: line});
                        stream.append(newLine, 'ul');
                        var el = newLine.view.$();
                        return el;
                    };

                    this.addLineScroll = function(e){
                        // fix to turn off if mouse action occurs
                        $('html, body').animate({
                            scrollTop: stream.addLine(e).offset().top
                        }, 200);
                    };

                    this.handleData = function(e){
                        console.log(e);
                        viz.data = e;
                    };

                    this.qutrLoad = function(e){
                        if (e.type === 'viz'){
                            console.log(e);
                            var newviz = $$(visual, {url:e.url});
                            stream.append(newviz);
                        }

                    };

                    socket.on("load", this.qutrLoad);
                    socket.on("stop", this.stop);
                    socket.on("lineOut", this.addLineScroll);
                    socket.on("dataOut", this.handleData);
                }
            }
        });


    $$.document.append(outputStream);
});
