$(document).ready(function() {
    var taskgroup = $$({}, {format: "taskgroup"},{}),
        task = $$({path:null},
                  {format:"task"},
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
                       this.view.render();
                       //jobrun.model.each(console.log);
                   },
                   'create': function(){
                       this.model.set({state:"Run"});
                   }
                  }).persist($$.adapter.restful, {collection:'tasks'}),

        job = $$({url:null, path:null},
                 {format:'<iframe data-bind="src=url"></iframe>'},
                 {'persist:save:succeess':function(){
                      console.log('burrito');
                      $$.document.append(this);
                  }
                 }).persist($$.adapter.restful, {collection:'jobs',
                                                 id:'uid'});

    $$.document.append(taskgroup
                       .persist()
                       .gather(task, 'append', 'dl'), '#container');
});