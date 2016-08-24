exports.leakMemory = function() {

  function LeakingClass() {
  }


  var leaks = [];
  setInterval(function() {
    for (var i = 0; i < 100; i++) {
      leaks.push(new LeakingClass);
    }

    console.error('Memory leaks: %d', leaks.length);
  }, 1000);
};

exports.buggyFunction = function(req, res) {
  
    
  var shouldRun = true;
  var desiredLoadFactor = .5;

  function blockCpuFor(ms) {
    var now = new Date().getTime();
    var result = 0
    while(shouldRun) {
      result += Math.random() * Math.random();
      if (new Date().getTime() > now +ms)
        return;
    }	
  }

  start = function(req) {
    shouldRun = true;
    blockCpuFor(1000*desiredLoadFactor);
    setTimeout(start, 1000* (1 - desiredLoadFactor));
  }


  exports.shouldRun = shouldRun;
  
  nonExistingFunction();
  
}


userNotFound = function(username) {
  
  // Justs prints a stack trace and explain that a given user doesn't exist
  console.log('Could not find user')
  err = new Error("Could not find user " + username);
  console.error(err.stack);
  
}

exports.findUser = function(req, res) {
  var username = req.params.username;
  
  userId = userNotFound(username);
    
}

exports.findNemo = function(req, res) {
 // if req?.params?.username { testvar = "something" } else { testvar = "something else" }
 
 var username = req.params.nemo
 userId = userNotFound(username, result);
  
}

exports.someBadMethod = function(req, res) {
  
  if (true) {
    // let's call some bad method
    var badness = badMethod();
  }

}
