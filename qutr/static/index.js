$(document).ready(function() {
    var task = $$({path:null},
                  {format:'<div class=\'task\'><dt> <strong data-bind="name" /> <br />'
                          + '<i data-bind="path"></i></dt>'
                          + '<dd><span data-bind="desc" /><br />'
                          + '</dd>'
                          + '<button class="launch">Run</button></div>'},
                  {'click &': function(e){
                       //@@ bind the button style too
                       this.model.set({state:"Stop"});

                       //@@ launch job
                       var path = this.model.get('path');

                       if (path === null){
                           // double call bug
                           return;
                       }
                       var jobrun = $$(job, {path:path});
                       jobrun.save();
                   },
                   'create': function(){
                       this.model.set({state:"Run"});
                   }
                  }).persist($$.adapter.restful, {collection:'tasks'}),

                      taskgroup = $$({},
                {format: "taskgroup"},
                    {'create':function(e) {}}),

        job = $$({url:null, path:null},
                 {format:
                         '<div class=\"\clearall">'
                         + '<p><button id="closer">close</button></p>'
                         + '<iframe data-bind="src=url" height="50%" scrolling="auto"></iframe>'
                         + '</div>'},
                 {'persist:save:success':function(){
                      this.model.set({url:"/" + this.model.get().id});
                      $$.document.append(this, '#container');
                  },
                  'click #closer': function(e){
                      this.destroy();
                  }
                 }).persist($$.adapter.restful, {collection:'jobs',
                 id:'uid'});
        taskgroup.persist().gather(task, 'append', '#tasklist');
        $$.document.append(taskgroup, '#container');
});