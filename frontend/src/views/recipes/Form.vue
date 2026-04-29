<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const recipeId = ref(route.params.id);
const isEditMode = ref(!!route.params.id);

const users = ref([]);
const tags = ref([]);
const newRecipeTitle = ref("");
const servings = ref("");
const description = ref("");
const user = ref("");
const selectedTags = ref([]);

const onSubmit = async() => {
    const formData = {
        user_id: user.value,
        title: newRecipeTitle.value,
        description: description.value,
        servings: servings.value,
        tag_ids: selectedTags.value
    }
    console.log(formData);

    if(isEditMode.value){
        await client.put(`/recipes/${recipeId.value}`, formData);
    }else{
        await client.post('/recipes', formData);
    }

    router.push('/recipes');
}

const fetchUsers = async() => {
    const response = await client.get('/users');
    users.value = response.data
}

const fetchTags = async() => {
    const response = await client.get('/tags');
    tags.value = response.data
}

onMounted(async () => {
    await fetchUsers();
    await fetchTags();

    if(isEditMode.value == true){
        const response = await client.get(`/recipes/${recipeId.value}`);
        newRecipeTitle.value = response.data.title;
        description.value = response.data.description;
        servings.value = response.data.servings;
        user.value = response.data.user_id;
        selectedTags.value = response.data.tags.map((t) => t.id);
    }
})
</script>

<template>
    <h1>{{ isEditMode ? "レシピ編集" : "レシピ新規追加" }}</h1>
    <div class="form-group">
        <input v-model="newRecipeTitle" placeholder="新しいレシピ名">
        <input
            v-model="servings"
            type="number"
        />

        <select v-model="user">
            <option disabled value="">ユーザーを選択</option>
            <option v-for="u in users" :key="u.id" :value="u.id">
                {{ u.username }}
            </option>
        </select>

        <div class="checkbox-list">
            <label v-for="t in tags" :key="t.id" class="checkbox-item">
                <input type="checkbox" v-model="selectedTags" :value="t.id">
                {{ t.title }}
            </label>
        </div>

        <textarea
            v-model="description"
            label="詳細"
            placeholder="入力してください"
        ></textarea>

        <button class="btn-submit" @click="onSubmit">{{ isEditMode ? "更新" : "登録" }}</button>
    </div>

    <router-link to="/recipes" class="btn-back">戻る</router-link>

</template>

<style scoped>
.form-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    max-width: 420px;
}

.form-group textarea,
.form-group select {
    padding: 8px 12px;
    border: 1px solid #d4b896;
    border-radius: 4px;
    font-size: 0.95rem;
    font-family: inherit;
    width: 260px;
    background: #fff;
    outline: none;
}

.form-group textarea {
    min-height: 90px;
    resize: vertical;
}

.form-group textarea:focus,
.form-group select:focus {
    border-color: #e8850c;
}

.checkbox-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 14px;
    width: 260px;
}

.checkbox-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    user-select: none;
    font-size: 0.95rem;
    color: #3d2e1f;
}

.checkbox-item input[type="checkbox"] {
    accent-color: #e8850c;
    cursor: pointer;
    margin: 0;
}
</style>
