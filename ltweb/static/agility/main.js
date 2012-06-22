var outputLine = $$({
                     model:{},
                     view:{
                         format: $('#lineformat').html()
                     },
                     controller: {}
                     });

var outputStream = $$({model:{},
                       view:{
                           format:$("#streamformat").html()
                       },
                       controller:{
                           'click #add': function(){
                               var newLine = $$(outputLine, {content:'wheeeee'});
                               this.append(newLine, 'ul');
                           }
                       }
                      });

$$.document.append(outputStream);