import { Router } from 'express';

import UserRoutes from './UserRoutes';

// Init router and path
const router = Router();

// Add sub-routes
router.use('/user', UserRoutes);

// Export the base-router
export default router;
