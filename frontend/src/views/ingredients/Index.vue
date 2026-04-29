<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter } from "vue-router";

const router = useRouter();
const ingredients = ref([]);

const goToEdit = (id) => {
    router.push({ name: "ingredients-edit", params: { id: id } });
};

const deleteIngredient = async(ingredient_id) => {
    await client.delete(`/ingredients/${ingredient_id}`);

    ingredients.value = ingredients.value.filter(i => i.id !== ingredient_id)
}

const fetchIngredients = async() => {
    const response = await client.get('/ingredients');
    ingredients.value = response.data;
}

onMounted(async () => {
    await fetchIngredients();
})
</script>

<template>
    <div class="page-header">
        <h1>食材一覧</h1>
        <router-link to="/ingredients/create" class="btn-submit">新規登録</router-link>
    </div>

    <!-- 食材一覧 -->
    <table class="tag-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>食材</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="ingredient in ingredients" :key="ingredient.id">
                <td>{{ ingredient.id }}</td>
                <td>{{ ingredient.name }}</td>
                <td class="tag-actions">
                    <button class="btn-edit" @click="goToEdit(ingredient.id)">編集</button>
                    <button class="btn-delete" @click="deleteIngredient(ingredient.id)">削除</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>
