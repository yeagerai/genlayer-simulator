-- Check environment
local function is_production()
    local env = os.getenv("ENVIRONMENT")
    return env and env:lower() == "prod"
end

-- Skip blocking if not in production
local is_prod = is_production()
ngx.log(ngx.DEBUG, "Environment check: ", is_prod and "prod" or "dev")
if not is_prod then
    return
end

-- List of blocked JSON-RPC methods
local blocked_methods = {
    "sim_clearDbTables",
    "sim_resetDefaultsLlmProviders",
    "sim_addProvider",
    "sim_updateProvider",
    "sim_deleteProvider",
    "sim_createValidator",
    "sim_createRandomValidator",
    "sim_createRandomValidators",
    "sim_updateValidator",
    "sim_deleteValidator",
    "sim_deleteAllValidators"
}

-- Convert array to hash table for O(1) lookup
local blocked_methods_hash = {}
for _, method in ipairs(blocked_methods) do
    blocked_methods_hash[method] = true
end

-- Get request body
ngx.req.read_body()
local body = ngx.req.get_body_data()

if body then
    -- Try to decode JSON
    local success, request = pcall(function()
        return require("cjson").decode(body)
    end)

    if success and request then
        -- Check if it's a JSON-RPC request
        if request.jsonrpc and request.method then
            -- Check if method is in blocked list
            if blocked_methods_hash[request.method] then
                -- Return JSON-RPC error response
                ngx.status = 403
                ngx.header.content_type = "application/json"
                ngx.say(require("cjson").encode({
                    jsonrpc = "2.0",
                    error = {
                        code = -32601,
                        message = "Method not allowed"
                    },
                    id = request.id
                }))
                return ngx.exit(ngx.HTTP_FORBIDDEN)
            end
        end
    end
end

-- Continue processing if method is not blocked
return