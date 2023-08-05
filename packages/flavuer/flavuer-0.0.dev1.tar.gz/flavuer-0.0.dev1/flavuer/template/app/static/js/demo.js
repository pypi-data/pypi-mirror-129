const Message = {
     data() {
         return {
             message: "VueJS is running as expected",
         }
     }
}
const app = Vue.createApp(Message);

// Define a new global component called button-counter
app.component('button-counter', {
    data() {
      return {
        count: 0
      }
    },
    template: `
      <button @click="count++">
        You clicked me {{ count }} times.
      </button>`
  });
app.mount("#app");
