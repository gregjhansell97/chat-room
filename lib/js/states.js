
class ItemState {
  constructor(item) {
    this.raw_item = item
    this.subscribers = {
      set: []
    }
  }
  expose() { return this.raw_item; }
  set(item) {
    this.raw_item = item;
    this.subscribers.set.forEach(f => f(item));
  }
  onSet(f) {this.subscribers.set.push(f)}
}
class ListState {
  constructor(l) {
    this.raw_list = l;
    this.subscribers = {
      push: [],
      remove: [],
      set: []
    }
  }
  push(item) {
    this.raw_list.push(item);
    this.subscribers.push.forEach(f => f(item));
  }
  remove(index) {
    this.raw_list.slice(index, 1);
    this.subscribers.remove.forEach(f => f(index));
  }
  set(l) {
    this.raw_list = l
    this.subscribers.set.forEach(f => f(l));
  }
  expose() { return this.raw_list; }
  onPush(f) { this.subscribers.push.push(f); }
  onRemove(f) { this.subscribers.remove.push(f);}
  onSet(f) { this.subscribers.set.push(f);}
}
