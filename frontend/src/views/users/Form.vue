<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const userId = ref(route.params.id);
const isEditMode = ref(!!route.params.id);

const newUsername = ref("");

const onSubmit = async() => {
    const formData = {
        username: newUsername.value
    }

    if(isEditMode.value){
        await client.put(`/users/${userId.value}`, formData);
    }else{
        await client.post('/users', formData);
    }

    router.push('/users');
}

onMounted(async () => {
    if(isEditMode.value == true){
        const response = await client.get(`/users/${userId.value}`);
        newUsername.value = response.data.username;
    }
})
</script>

<template>
    <h1>{{ isEditMode ? "ユーザー編集" : "ユーザー新規登録" }}</h1>
    <div class="form-group">
        <input v-model="newUsername" placeholder="新しいユーザー名" />
        <button class="btn-submit" @click="onSubmit">{{ isEditMode ? "更新" : "登録" }}</button>
    </div>
    <router-link to="/users" class="btn-back">← 戻る</router-link>
</template>
