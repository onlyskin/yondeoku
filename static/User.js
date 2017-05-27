class User {
  constructor(userdata) {
    this._userdata = userdata;
  }

  get userdata() {
    return this._userdata;
  }

  get known() {
    return this.userdata.known;
  }

  get username() {
    return this.userdata.username;
  }

  get threshold() {
    return this.userdata.threshold;
  }

  get blocks() {
    return this.userdata.blocks;
  }

  get_known(language) {
    var known = this.known;
    var filtered = known.filter(function (w) {
      return w.language === language;
    });
    filtered.sort(function(a, b) {
      if (a.word < b.word)
        return -1;
      if (a.word > b.word)
        return 1;
      return 0;
    });
    return filtered;
  }

  get_block(id) {
    var block = this.blocks.filter(function(b) {return b.id == id;})[0]
    return block;
  }
}