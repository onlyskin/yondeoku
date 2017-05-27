class Block {
  constructor(block) {
    this._blockdata = block;
  }

  get blockdata() {
    return this._blockdata;
  }

  get sections() {
    return this.blockdata.sections;
  }

  get_next_unread_section_index(startIndex) {
    return this.blockdata.readSections.indexOf(false, startIndex);
  }

  get_section_lemmas(index) {
    return this.blockdata.sections[index].lemmas;
  }

  get_next_unread_section_lemmas(startIndex) {
    var index = this.get_next_unread_section_index(0);
    return this.get_section_lemmas(index);
  }

}