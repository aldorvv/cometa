<!-- App.vue -->

<template>
  <div>
    <DropdownMenu :options="dropdownOptions" @select="handleSelect" />
    <label class="apple-font">
      <input type="checkbox" v-model="split" />
      Go dutch
    </label>
    <DebtDisplay :response="response" />
    <label class="apple-font">
      Va a pagar:
      <input type="number" v-model="quantityToPay" min="1"/>
      USD
    </label>
    <button class="pay-button" @click="handlePayment">Pagar</button>
  </div>
</template>

<script>
import DropdownMenu from './components/DropdownMenu.vue';
import DebtDisplay from './components/DebtDisplay.vue';
import axios from 'axios';

export default {
  components: {
    DropdownMenu,
    DebtDisplay,
  },
  data() {
    return {
      dropdownOptions: ['Scott Pilgrim', 'Kim Pine', 'Stephen Stills'],
      selectedOption: "",
      response: "",
      split: false,
      quantityToPay: 0,
      money: {
        'Scott Pilgrim': 0,
        'Kim Pine': 0,
        'Stephen Stills': 0
      }
    };
  },
  methods: {
    isPaymentReady() {
      for (const key in this.money) {
        if (Object.hasOwnProperty.call(this.money, key)) {
          if (this.money[key] <= 0) {
            return false;
          }
        }
      }
      return true;
    },
    async handleSelect(option) {
      this.selectedOption = option;
      this.fetch();
    },
    async fetch() {
      try {
        if (this.selectedOption) {
          const split = this.split ? '?split=False' : '';
          const response = await axios.get(`http://localhost:8000/bills/1/debts${split}`);
          const debt = (response.data[this.selectedOption] / 100) - this.money[this.selectedOption];
          this.response = `${this.selectedOption} debe ${debt >= 0 ? debt : 0} USD`;
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async handlePayment() {
      try {
        if (this.quantityToPay && this.selectedOption) {
          const split = this.split ? '?split=False' : '';
          this.money[this.selectedOption] = this.quantityToPay;
          const response = await axios.get(`http://localhost:8000/bills/1/debts${split}`);
          const debt = (response.data[this.selectedOption] / 100) - this.money[this.selectedOption];
          this.response = `${this.selectedOption} debe ${debt >= 0 ? debt : 0} USD`;

          if (this.isPaymentReady()) {
            const data = this.dropdownOptions.map((name) => {
              return {
                customer: name,
                amount: this.money[name]
              };
            })
            const r = await axios.patch(`http://localhost:8000/bills/1/pay${split}`, data, {headers: {"Content-Type": "application/json"}});

            if (r.status == 200) {
              alert("Cuenta pagada 🎉");
            }
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
  },
  watch: {
    split: 'fetch',
  }
};
</script>

<style scoped>
.apple-font {
  font-family: 'San Francisco', sans-serif;
  margin-left: 10px;
}

.pay-button {
  background-color: #3498db;
  color: #fff;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

</style>