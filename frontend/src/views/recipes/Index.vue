<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter } from "vue-router";

const router = useRouter();
const recipes = ref([]);

const goToEdit = (id) => {
    router.push({ name: "recipes-edit", params: { id: id } });
};

const deleteRecipe = async(recipe_id) => {
    await client.delete(`/recipes/${recipe_id}`);

    recipes.value = recipes.value.filter(r => r.id !== recipe_id)
}

const fetchRecipes = async() => {
    const response = await client.get('/recipes');
    recipes.value = response.data;
}

onMounted(async () => {
    fetchRecipes();
})

</script>

<template>
    <div class="page-header">
        <h1>レシピ一覧</h1>
        <router-link to="/recipes/create" class="btn-submit">新規登録</router-link>
    </div>

    <!-- レシピ一覧 -->
    <table class="tag-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>料理名</th>
                <th>詳細</th>
                <th>何人前</th>
                <th>タグ</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="recipe in recipes" :key="recipe.recipe_id">
                <td>{{ recipe.id }}</td>
                <td>{{ recipe.title }}</td>
                <td>{{ recipe.description }}</td>
                <td>{{ recipe.servings }}</td>
                <td>                                                                                                              
                    <span v-for="tag in recipe.tags" :key="tag.id" class="tag-badge">                                             
                        {{ tag.title }}                     
                    </span>                                                                                                       
                </td>   
                <td class="tag-actions">
                    <button class="btn-edit" @click="goToEdit(recipe.id)">編集</button>
                    <button class="btn-delete" @click="deleteRecipe(recipe.id)">削除</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>
