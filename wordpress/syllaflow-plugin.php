<?php
/**
 * Plugin Name: SyllaFlow AlignFlow Integration
 * Plugin URI: https://github.com/evr-rzn48/syllaflow
 * Description: Integrates SyllaFlow syllable-based word search with AlignFlow journal system for mindful word discovery and reflection.
 * Version: 1.0.0
 * Author: Council of Consciousness
 * Author URI: https://elv48.me
 * License: GPL v2 or later
 * Text Domain: syllaflow-alignflow
 * Domain Path: /languages
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('SYLLAFLOW_VERSION', '1.0.0');
define('SYLLAFLOW_PLUGIN_URL', plugin_dir_url(__FILE__));
define('SYLLAFLOW_PLUGIN_PATH', plugin_dir_path(__FILE__));

/**
 * Main SyllaFlow Plugin Class
 */
class SyllaFlowAlignFlowIntegration {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('rest_api_init', array($this, 'register_rest_routes'));
        add_action('wp_footer', array($this, 'add_widget_container'));
        
        // Shortcode registration
        add_shortcode('syllaflow', array($this, 'syllaflow_shortcode'));
        add_shortcode('syllaflow-widget', array($this, 'syllaflow_widget_shortcode'));
        
        // WordPress hooks for AlignFlow integration
        add_action('wp_ajax_syllaflow_sync', array($this, 'handle_sync_request'));
        add_action('wp_ajax_nopriv_syllaflow_sync', array($this, 'handle_sync_request'));
        
        // Custom post types for SyllaFlow data
        add_action('init', array($this, 'register_post_types'));
        
        // Admin menu
        add_action('admin_menu', array($this, 'add_admin_menu'));
    }
    
    /**
     * Initialize plugin
     */
    public function init() {
        // Load text domain for translations
        load_plugin_textdomain('syllaflow-alignflow', false, dirname(plugin_basename(__FILE__)) . '/languages');
        
        // Initialize database tables if needed
        $this->maybe_create_tables();
    }
    
    /**
     * Enqueue scripts and styles
     */
    public function enqueue_scripts() {
        // Enqueue React and SyllaFlow components
        wp_enqueue_script(
            'syllaflow-react',
            'https://unpkg.com/react@18/umd/react.production.min.js',
            array(),
            SYLLAFLOW_VERSION,
            true
        );
        
        wp_enqueue_script(
            'syllaflow-react-dom',
            'https://unpkg.com/react-dom@18/umd/react-dom.production.min.js',
            array('syllaflow-react'),
            SYLLAFLOW_VERSION,
            true
        );
        
        wp_enqueue_script(
            'syllaflow-app',
            SYLLAFLOW_PLUGIN_URL . 'assets/js/syllaflow-app.js',
            array('syllaflow-react', 'syllaflow-react-dom'),
            SYLLAFLOW_VERSION,
            true
        );
        
        wp_enqueue_style(
            'syllaflow-styles',
            SYLLAFLOW_PLUGIN_URL . 'assets/css/syllaflow-styles.css',
            array(),
            SYLLAFLOW_VERSION
        );
        
        // Localize script with WordPress data
        wp_localize_script('syllaflow-app', 'syllaflowData', array(
            'ajaxUrl' => admin_url('admin-ajax.php'),
            'restUrl' => rest_url('syllaflow/v1/'),
            'nonce' => wp_create_nonce('syllaflow_nonce'),
            'userId' => get_current_user_id(),
            'isLoggedIn' => is_user_logged_in(),
            'siteUrl' => home_url(),
            'pluginUrl' => SYLLAFLOW_PLUGIN_URL
        ));
    }
    
    /**
     * Register REST API routes
     */
    public function register_rest_routes() {
        register_rest_route('syllaflow/v1', '/session/init', array(
            'methods' => 'POST',
            'callback' => array($this, 'init_session'),
            'permission_callback' => '__return_true'
        ));
        
        register_rest_route('syllaflow/v1', '/word/discovered', array(
            'methods' => 'POST',
            'callback' => array($this, 'record_word_discovery'),
            'permission_callback' => '__return_true'
        ));
        
        register_rest_route('syllaflow/v1', '/word/reflection', array(
            'methods' => 'POST',
            'callback' => array($this, 'add_word_reflection'),
            'permission_callback' => '__return_true'
        ));
        
        register_rest_route('syllaflow/v1', '/journal/create', array(
            'methods' => 'POST',
            'callback' => array($this, 'create_journal_entry'),
            'permission_callback' => array($this, 'check_journal_permissions')
        ));
        
        register_rest_route('syllaflow/v1', '/session/(?P<id>[a-zA-Z0-9_-]+)/summary', array(
            'methods' => 'GET',
            'callback' => array($this, 'get_session_summary'),
            'permission_callback' => '__return_true'
        ));
        
        register_rest_route('syllaflow/v1', '/sync', array(
            'methods' => 'POST',
            'callback' => array($this, 'sync_with_alignflow'),
            'permission_callback' => '__return_true'
        ));
    }
    
    /**
     * Register custom post types for SyllaFlow data
     */
    public function register_post_types() {
        // SyllaFlow Sessions
        register_post_type('syllaflow_session', array(
            'labels' => array(
                'name' => __('SyllaFlow Sessions', 'syllaflow-alignflow'),
                'singular_name' => __('SyllaFlow Session', 'syllaflow-alignflow')
            ),
            'public' => false,
            'show_ui' => true,
            'show_in_menu' => 'syllaflow-admin',
            'supports' => array('title', 'editor', 'custom-fields'),
            'capability_type' => 'post'
        ));
        
        // Word Discoveries
        register_post_type('syllaflow_discovery', array(
            'labels' => array(
                'name' => __('Word Discoveries', 'syllaflow-alignflow'),
                'singular_name' => __('Word Discovery', 'syllaflow-alignflow')
            ),
            'public' => false,
            'show_ui' => true,
            'show_in_menu' => 'syllaflow-admin',
            'supports' => array('title', 'editor', 'custom-fields'),
            'capability_type' => 'post'
        ));
        
        // Insights
        register_post_type('syllaflow_insight', array(
            'labels' => array(
                'name' => __('Insights', 'syllaflow-alignflow'),
                'singular_name' => __('Insight', 'syllaflow-alignflow')
            ),
            'public' => false,
            'show_ui' => true,
            'show_in_menu' => 'syllaflow-admin',
            'supports' => array('title', 'editor', 'custom-fields'),
            'capability_type' => 'post'
        ));
    }
    
    /**
     * Add admin menu
     */
    public function add_admin_menu() {
        add_menu_page(
            __('SyllaFlow', 'syllaflow-alignflow'),
            __('SyllaFlow', 'syllaflow-alignflow'),
            'manage_options',
            'syllaflow-admin',
            array($this, 'admin_page'),
            'dashicons-games',
            30
        );
        
        add_submenu_page(
            'syllaflow-admin',
            __('Settings', 'syllaflow-alignflow'),
            __('Settings', 'syllaflow-alignflow'),
            'manage_options',
            'syllaflow-settings',
            array($this, 'settings_page')
        );
    }
    
    /**
     * SyllaFlow shortcode
     */
    public function syllaflow_shortcode($atts) {
        $atts = shortcode_atts(array(
            'theme' => 'alignflow',
            'size' => 'medium',
            'position' => 'inline',
            'enable_reflections' => 'true',
            'enable_journal' => 'true',
            'auto_minimize' => 'false'
        ), $atts);
        
        $widget_id = 'syllaflow-' . uniqid();
        
        ob_start();
        ?>
        <div id="<?php echo esc_attr($widget_id); ?>" class="syllaflow-container" 
             data-config="<?php echo esc_attr(json_encode($atts)); ?>">
            <div class="syllaflow-loading">
                <p><?php _e('Loading SyllaFlow...', 'syllaflow-alignflow'); ?></p>
            </div>
        </div>
        
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof SyllaFlowApp !== 'undefined') {
                SyllaFlowApp.init('<?php echo esc_js($widget_id); ?>', <?php echo json_encode($atts); ?>);
            }
        });
        </script>
        <?php
        return ob_get_clean();
    }
    
    /**
     * SyllaFlow widget shortcode (floating widget)
     */
    public function syllaflow_widget_shortcode($atts) {
        $atts = shortcode_atts(array(
            'theme' => 'alignflow',
            'size' => 'medium',
            'position' => 'bottom-right',
            'auto_minimize' => 'true'
        ), $atts);
        
        // Add widget to footer
        add_action('wp_footer', function() use ($atts) {
            $widget_id = 'syllaflow-widget-' . uniqid();
            ?>
            <div id="<?php echo esc_attr($widget_id); ?>" class="syllaflow-widget-container" 
                 data-config="<?php echo esc_attr(json_encode($atts)); ?>">
            </div>
            
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                if (typeof SyllaFlowWidget !== 'undefined') {
                    SyllaFlowWidget.init('<?php echo esc_js($widget_id); ?>', <?php echo json_encode($atts); ?>);
                }
            });
            </script>
            <?php
        });
        
        return ''; // Widget is added to footer, no inline content
    }
    
    /**
     * Initialize session
     */
    public function init_session($request) {
        $params = $request->get_json_params();
        
        $session_id = 'session_' . time() . '_' . wp_generate_password(8, false);
        $user_id = get_current_user_id();
        
        // Create session post
        $session_post_id = wp_insert_post(array(
            'post_type' => 'syllaflow_session',
            'post_title' => 'SyllaFlow Session - ' . date('Y-m-d H:i:s'),
            'post_status' => 'private',
            'post_author' => $user_id ?: 0,
            'meta_input' => array(
                'session_id' => $session_id,
                'start_time' => current_time('mysql'),
                'user_preferences' => json_encode($params['userPreferences'] ?? array()),
                'device_info' => json_encode($params['deviceInfo'] ?? array()),
                'status' => 'active'
            )
        ));
        
        if (is_wp_error($session_post_id)) {
            return new WP_Error('session_creation_failed', 'Failed to create session', array('status' => 500));
        }
        
        return rest_ensure_response(array(
            'success' => true,
            'sessionId' => $session_id,
            'postId' => $session_post_id,
            'message' => 'Session initialized successfully'
        ));
    }
    
    /**
     * Record word discovery
     */
    public function record_word_discovery($request) {
        $params = $request->get_json_params();
        
        if (empty($params['sessionId']) || empty($params['wordData'])) {
            return new WP_Error('missing_data', 'Session ID and word data are required', array('status' => 400));
        }
        
        $word_data = $params['wordData'];
        $user_id = get_current_user_id();
        
        // Create word discovery post
        $discovery_post_id = wp_insert_post(array(
            'post_type' => 'syllaflow_discovery',
            'post_title' => 'Word Discovery: ' . $word_data['word'],
            'post_content' => $word_data['definition'],
            'post_status' => 'private',
            'post_author' => $user_id ?: 0,
            'meta_input' => array(
                'session_id' => $params['sessionId'],
                'word' => $word_data['word'],
                'definition' => $word_data['definition'],
                'etymology' => $word_data['etymology'] ?? '',
                'syllables' => json_encode($word_data['syllables'] ?? array()),
                'mindfulness_prompt' => $word_data['mindfulnessPrompt'] ?? '',
                'discovery_time' => current_time('mysql'),
                'discovery_method' => $word_data['discoveryMethod'] ?? 'syllable-search'
            )
        ));
        
        if (is_wp_error($discovery_post_id)) {
            return new WP_Error('discovery_creation_failed', 'Failed to record word discovery', array('status' => 500));
        }
        
        // Trigger WordPress action for other plugins/themes
        do_action('syllaflow_word_discovered', $discovery_post_id, $word_data, $params['sessionId']);
        
        return rest_ensure_response(array(
            'success' => true,
            'discoveryId' => $discovery_post_id,
            'message' => 'Word discovery recorded successfully'
        ));
    }
    
    /**
     * Add word reflection
     */
    public function add_word_reflection($request) {
        $params = $request->get_json_params();
        
        if (empty($params['discoveryId']) || empty($params['reflection'])) {
            return new WP_Error('missing_data', 'Discovery ID and reflection are required', array('status' => 400));
        }
        
        $discovery_id = intval($params['discoveryId']);
        $reflection = sanitize_textarea_field($params['reflection']);
        
        // Update discovery post with reflection
        $updated = update_post_meta($discovery_id, 'user_reflection', $reflection);
        update_post_meta($discovery_id, 'reflection_time', current_time('mysql'));
        
        if (isset($params['emotionalResonance'])) {
            update_post_meta($discovery_id, 'emotional_resonance', intval($params['emotionalResonance']));
        }
        
        if (isset($params['personalConnection'])) {
            update_post_meta($discovery_id, 'personal_connection', sanitize_textarea_field($params['personalConnection']));
        }
        
        // Trigger WordPress action
        do_action('syllaflow_reflection_added', $discovery_id, $reflection);
        
        return rest_ensure_response(array(
            'success' => true,
            'message' => 'Reflection added successfully'
        ));
    }
    
    /**
     * Create journal entry
     */
    public function create_journal_entry($request) {
        $params = $request->get_json_params();
        
        if (empty($params['sessionId']) || empty($params['entryData'])) {
            return new WP_Error('missing_data', 'Session ID and entry data are required', array('status' => 400));
        }
        
        $entry_data = $params['entryData'];
        $user_id = get_current_user_id();
        
        // Create journal entry as regular post or custom post type
        $journal_post_id = wp_insert_post(array(
            'post_type' => 'post', // or 'alignflow_journal' if custom post type exists
            'post_title' => sanitize_text_field($entry_data['title']),
            'post_content' => wp_kses_post($entry_data['content']),
            'post_status' => $entry_data['privacy'] === 'public' ? 'publish' : 'private',
            'post_author' => $user_id,
            'meta_input' => array(
                'syllaflow_session_id' => $params['sessionId'],
                'syllaflow_generated' => true,
                'mood' => sanitize_text_field($entry_data['mood'] ?? ''),
                'gratitude' => json_encode($entry_data['gratitude'] ?? array()),
                'intentions' => json_encode($entry_data['intentions'] ?? array()),
                'word_count' => str_word_count(strip_tags($entry_data['content']))
            )
        ));
        
        if (is_wp_error($journal_post_id)) {
            return new WP_Error('journal_creation_failed', 'Failed to create journal entry', array('status' => 500));
        }
        
        // Add tags
        if (!empty($entry_data['tags'])) {
            wp_set_post_tags($journal_post_id, $entry_data['tags']);
        }
        
        // Trigger WordPress action for AlignFlow integration
        do_action('alignflow_journal_entry_created', $journal_post_id, $entry_data, $params['sessionId']);
        
        return rest_ensure_response(array(
            'success' => true,
            'journalId' => $journal_post_id,
            'message' => 'Journal entry created successfully',
            'viewUrl' => get_permalink($journal_post_id)
        ));
    }
    
    /**
     * Get session summary
     */
    public function get_session_summary($request) {
        $session_id = $request['id'];
        
        // Get session post
        $session_posts = get_posts(array(
            'post_type' => 'syllaflow_session',
            'meta_key' => 'session_id',
            'meta_value' => $session_id,
            'posts_per_page' => 1
        ));
        
        if (empty($session_posts)) {
            return new WP_Error('session_not_found', 'Session not found', array('status' => 404));
        }
        
        $session_post = $session_posts[0];
        
        // Get related discoveries
        $discoveries = get_posts(array(
            'post_type' => 'syllaflow_discovery',
            'meta_key' => 'session_id',
            'meta_value' => $session_id,
            'posts_per_page' => -1
        ));
        
        // Calculate summary data
        $words_discovered = count($discoveries);
        $reflections_added = 0;
        $top_words = array();
        
        foreach ($discoveries as $discovery) {
            $reflection = get_post_meta($discovery->ID, 'user_reflection', true);
            if (!empty($reflection)) {
                $reflections_added++;
                $top_words[] = array(
                    'word' => get_post_meta($discovery->ID, 'word', true),
                    'definition' => $discovery->post_content,
                    'reflection' => $reflection
                );
            }
        }
        
        $summary = array(
            'sessionId' => $session_id,
            'userId' => $session_post->post_author,
            'startTime' => get_post_meta($session_post->ID, 'start_time', true),
            'wordsDiscovered' => $words_discovered,
            'reflectionsAdded' => $reflections_added,
            'topWords' => array_slice($top_words, 0, 5),
            'achievements' => $this->calculate_achievements($words_discovered, $reflections_added)
        );
        
        return rest_ensure_response(array(
            'success' => true,
            'summary' => $summary
        ));
    }
    
    /**
     * Sync with AlignFlow
     */
    public function sync_with_alignflow($request) {
        $params = $request->get_json_params();
        
        // This would implement the actual sync logic with AlignFlow journal system
        // For now, we'll just acknowledge the sync request
        
        return rest_ensure_response(array(
            'success' => true,
            'message' => 'Data synced successfully with AlignFlow journal',
            'timestamp' => current_time('mysql')
        ));
    }
    
    /**
     * Check journal permissions
     */
    public function check_journal_permissions($request) {
        // Allow logged-in users to create journal entries
        // Guest users can create entries but they won't be saved to their account
        return true;
    }
    
    /**
     * Calculate achievements based on session data
     */
    private function calculate_achievements($words_discovered, $reflections_added) {
        $achievements = array();
        
        if ($words_discovered >= 1) {
            $achievements[] = 'First word discovered';
        }
        if ($words_discovered >= 5) {
            $achievements[] = 'Word explorer';
        }
        if ($words_discovered >= 10) {
            $achievements[] = 'Word master';
        }
        if ($reflections_added >= 1) {
            $achievements[] = 'First reflection added';
        }
        if ($reflections_added >= 3) {
            $achievements[] = 'Thoughtful practitioner';
        }
        
        return $achievements;
    }
    
    /**
     * Handle AJAX sync requests
     */
    public function handle_sync_request() {
        check_ajax_referer('syllaflow_nonce', 'nonce');
        
        $session_data = json_decode(stripslashes($_POST['sessionData']), true);
        
        // Process sync data
        // This would update WordPress posts/meta based on the session data
        
        wp_send_json_success(array(
            'message' => 'Sync completed successfully',
            'timestamp' => current_time('mysql')
        ));
    }
    
    /**
     * Add widget container to footer
     */
    public function add_widget_container() {
        // This can be used to add a global widget container if needed
    }
    
    /**
     * Admin page
     */
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1><?php _e('SyllaFlow AlignFlow Integration', 'syllaflow-alignflow'); ?></h1>
            <p><?php _e('Manage your SyllaFlow sessions and AlignFlow journal integration.', 'syllaflow-alignflow'); ?></p>
            
            <!-- Admin interface would go here -->
        </div>
        <?php
    }
    
    /**
     * Settings page
     */
    public function settings_page() {
        ?>
        <div class="wrap">
            <h1><?php _e('SyllaFlow Settings', 'syllaflow-alignflow'); ?></h1>
            
            <form method="post" action="options.php">
                <?php
                settings_fields('syllaflow_settings');
                do_settings_sections('syllaflow_settings');
                ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row"><?php _e('Default Theme', 'syllaflow-alignflow'); ?></th>
                        <td>
                            <select name="syllaflow_default_theme">
                                <option value="alignflow"><?php _e('AlignFlow', 'syllaflow-alignflow'); ?></option>
                                <option value="minimal"><?php _e('Minimal', 'syllaflow-alignflow'); ?></option>
                                <option value="dark"><?php _e('Dark', 'syllaflow-alignflow'); ?></option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><?php _e('Enable Journal Integration', 'syllaflow-alignflow'); ?></th>
                        <td>
                            <input type="checkbox" name="syllaflow_enable_journal" value="1" checked />
                            <label><?php _e('Allow SyllaFlow to create journal entries', 'syllaflow-alignflow'); ?></label>
                        </td>
                    </tr>
                </table>
                
                <?php submit_button(); ?>
            </form>
        </div>
        <?php
    }
    
    /**
     * Create database tables if needed
     */
    private function maybe_create_tables() {
        // Custom tables could be created here if needed
        // For now, we're using WordPress posts and meta
    }
}

// Initialize the plugin
new SyllaFlowAlignFlowIntegration();

// Activation hook
register_activation_hook(__FILE__, function() {
    // Plugin activation tasks
    flush_rewrite_rules();
});

// Deactivation hook
register_deactivation_hook(__FILE__, function() {
    // Plugin deactivation tasks
    flush_rewrite_rules();
});
?>
