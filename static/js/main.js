const { createApp } = Vue;

createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      users: [],
      newUsername: '',
      editingId: null,
      editedName: '',
    };
  },
  methods: {
    fetchUsers() {
      fetch('/api/users')
        .then((res) => res.json())
        .then((data) => {
          this.users = data;
        });
    },
    addUser() {
      const username = this.newUsername.trim();
      if (!username) return;

      fetch('/api/add_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.user) {
            this.users.push(data.user);
            this.newUsername = '';
          }
        });
    },
    deleteUser(id) {
      if (!confirm('本当に削除しますか？')) return;
      fetch(`/api/delete/${id}`, { method: 'DELETE' }).then(() => {
        this.users = this.users.filter((u) => u.id !== id);
      });
    },
    startEdit(user) {
      this.editingId = user.id;
      this.editedName = user.username;
    },
    cancelEdit() {
      this.editingId = null;
      this.editedName = '';
    },
    updateUser(id) {
      const newName = this.editedName.trim();
      if (!newName) return;

      fetch(`/api/update/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: newName }),
      })
        .then((res) => res.json())
        .then((data) => {
          const updated = data.user;
          const target = this.users.find((u) => u.id === id);
          if (target) target.username = updated.username;
          this.cancelEdit();
        });
    },
  },
  mounted() {
    this.fetchUsers();
  },
}).mount('#app');
