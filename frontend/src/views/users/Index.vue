<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter } from "vue-router";

const router = useRouter();
const users = ref([])

const goToEdit = (id) => {
    router.push({ name: "users-edit", params: { id: id } });
};

const deleteUser = async(user_id) => {
    await client.delete(`/users/${user_id}`);

    users.value = users.value.filter(u => u.id !== user_id)
}

const fetchUsers = async() => {
    const response = await client.get('/users');
    users.value = response.data
}

onMounted(async() => {
    await fetchUsers();
})
</script>

<template>
    <div class="page-header">
        <h1>ユーザー一覧</h1>
        <router-link to="/users/create" class="btn-submit">新規登録</router-link>
    </div>

    <!-- ユーザー一覧 -->
    <table class="tag-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>ユーザー名</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td class="tag-actions">
                    <button class="btn-edit" @click="goToEdit(user.id)">編集</button>
                    <button class="btn-delete" @click="deleteUser(user.id)">削除</button>
                </td>
            </tr>
        </tbody>
    </table>

</template>
