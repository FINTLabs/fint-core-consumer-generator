package no.fintlabs.consumer.model.MODEL_LOWER;

import no.fint.model.felles.kompleksedatatyper.Identifikator;
import no.fint.model.resource.DOMAIN.PACKAGE.MODEL_RESOURCE;
import no.fintlabs.cache.Cache;
import no.fintlabs.cache.CacheManager;
import no.fintlabs.cache.packing.PackingTypes;
import no.fintlabs.core.consumer.shared.resource.CacheService;
import no.fintlabs.core.consumer.shared.resource.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.util.Optional;

@Service
public class MODELService extends CacheService<MODEL_RESOURCE> {

    private final MODELKafkaConsumer MODEL_LOWERKafkaConsumer;

    private final MODELLinker linker;

    public MODELService(
            MODELConfig MODEL_LOWERConfig,
            CacheManager cacheManager,
            MODELKafkaConsumer MODEL_LOWERKafkaConsumer,
            MODELLinker linker) {
        super(MODEL_LOWERConfig, cacheManager, MODEL_LOWERKafkaConsumer);
        this.MODEL_LOWERKafkaConsumer = MODEL_LOWERKafkaConsumer;
        this.linker = linker;
    }

    @Override
    protected Cache<MODEL_RESOURCE> initializeCache(CacheManager cacheManager, ConsumerConfig<MODEL_RESOURCE> consumerConfig, String s) {
        return cacheManager.create(PackingTypes.POJO, consumerConfig.getOrgId(), consumerConfig.getResourceName());
    }

    @PostConstruct
    private void registerKafkaListener() {
        long retension = MODEL_LOWERKafkaConsumer.registerListener(MODEL_RESOURCE.class, this::addResourceToCache);
        getCache().setRetentionPeriodInMs(retension);
    }

    private void addResourceToCache(ConsumerRecord<String, MODEL_RESOURCE> consumerRecord) {
        this.eventLogger.logDataRecieved();
        if (consumerRecord.value() == null) {
            getCache().remove(consumerRecord.key());
        } else {
            MODEL_RESOURCE MODEL_LOWERResource = consumerRecord.value();
            linker.mapLinks(MODEL_LOWERResource);
            getCache().put(consumerRecord.key(), MODEL_LOWERResource, linker.hashCodes(MODEL_LOWERResource));
        }
    }

    @Override
    public Optional<MODEL_RESOURCE> getBySystemId(String systemId) {
        return getCache().getLastUpdatedByFilter(systemId.hashCode(),
                resource -> Optional
                        .ofNullable(resource)
                        .map(MODEL_RESOURCE::getSystemId)
                        .map(Identifikator::getIdentifikatorverdi)
                        .map(systemId::equals)
                        .orElse(false));
    }
}