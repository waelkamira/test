// scraper.js

import {
  searchRecipes,
  MarmitonQueryBuilder,
  RECIPE_PRICE,
  RECIPE_DIFFICULTY,
} from 'marmiton-api';

const qb = new MarmitonQueryBuilder();

const query = qb
  .withTitleContaining('soja') // يمكن تغيير 'soja' إلى أي كلمة بحث أخرى
  .withoutOven()
  .withPrice(RECIPE_PRICE.CHEAP)
  .takingLessThan(45)
  .withDifficulty(RECIPE_DIFFICULTY.EASY)
  .build();

(async () => {
  try {
    // جلب الوصفات
    const recipes = await searchRecipes(query, { limit: 48 });

    // عرض النتائج
    console.log('Fetched Recipes:', recipes);
  } catch (error) {
    console.error('Error fetching recipes:', error);
  }
})();
